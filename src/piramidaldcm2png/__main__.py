"""
This is the main module of the 'piramidaldicom2png' package. 

The package is designed to convert one level of a pyramidal DICOM (Digital Imaging and Communications in Medicine) file into a group of PNG (Portable Network Graphics) images. 

This conversion is particularly useful in medical imaging where DICOM is the standard format. However, for certain applications like machine learning models or web visualization, PNG format might be more suitable due to its wide acceptance and smaller size.

The 'piramidaldicom2png' package provides a command-line interface (CLI) for easy conversion of these files. The CLI is installed as 'fibonacci' in the current environment when the package is installed.

Please refer to the following links for more information on entry points and pip installation:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install

"""

import argparse
import json
import logging
import sys

from pathlib import Path

import PIL
import pydicom

from piramidaldcm2png import __version__
from dcm2mids.get_dicomdir import get_dicomdir
from dcm2mids.procedures.dictify import dictify


__author__ = "jomasator2"
__copyright__ = "jomasator2"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from piramidaldcm2png.skeleton import fib`,
# when using this Python module as a library.


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description='Convert a level of a pyramidal DICOM from a BIDS/MIDS project into a group of PNG images.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument(
        "-p",
        '--project',
        required=True,
        type=Path,
        help='Path to the BIDS/MIDS project to convert.',
    )
    
    group.add_argument(
        "-l",
        '--level',
        type=int,
        default=0,
        required=False,
        help='''The level in the pyramidal DICOM determined by the resolution order in tag 0x0029, 0x1010. 
        The first level is the layer with the lowest resolution, the second is 
        the second, and so on. Negative values can be used to access the last 
        elements. ''',
    )

    group.add_argument(
        "-c",
        '--chunk',
        type=int,
        default=0,
        required=False,
        help='The level in the pyramidal DICOM determined by the Chunk variable in the naming convention of BIDS/MIDS',
    )
    
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    
    return parser.parse_args()

def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def search_by_resolution_order(project, level, path_to_save):
    paths_dicom = project.resolve().rglob("sub*chunk-1_BF.dcm")
    
    for path in paths_dicom:
        print(path)
        fs = get_dicomdir(path.parent)
        dataset = fs.find(InstanceNumber=1)[0].load()
        levels_list = dataset[0x29,0x1010].value
        UID, number_of_frames = levels_list[-1*level][0x29, 0x1061][0]
        fileset = fs.find(SOPInstanceUID=UID.value)[0]
        dataset = fs.find(SOPInstanceUID=UID.value)[0].load()
        pixel_data = dataset.pixel_array
        for i_crop in range(number_of_frames.value):
            path_to_save_crop = path_to_save.joinpath(
                path.relative_to(project).parent, 
                f"{path.stem.split('_run')[0]}_run-{dataset.SeriesNumber}_chunk-{dataset.InstanceNumber}_mod-BF_desc-{i_crop+1:03}_crop.png"
            )
            path_to_save_crop.parent.mkdir(parents=True, exist_ok=True)
            image = pixel_data[i_crop]
            PIL.Image.fromarray(image, 'YCbCr').convert('RGB').save(path_to_save_crop)
        with path_to_save_crop.with_suffix(".json").open("w") as json_file:
            json.dump(dictify(dataset), json_file, indent=4)

def search_by_chunk(project, chunk, path_to_save):
    paths_dicom = project.resolve().rglob(f"sub*chunk-{chunk}_BF.dcm")
    
    
    for path in paths_dicom:
        print(path)
        dicom = pydicom.dcmread(path)
        dicom_image = dicom.pixel_array
        for i_crop in range(dicom.NumberOfFrames):
            path_to_save_crop = path_to_save.joinpath(
                path.relative_to(project).parent, 
                f"{path.stem.split('_run')[0]}_run-{dicom.SeriesNumber}_chunk-{dicom.InstanceNumber}_mod-BF_desc-{i_crop+1:03}_crop.png"
            )
            path_to_save_crop.parent.mkdir(parents=True, exist_ok=True)
            image = dicom_image[i_crop]
            PIL.Image.fromarray(image, 'YCbCr').convert('RGB').save(path_to_save_crop)
        with path_to_save_crop.with_suffix(".json").open("w") as json_file:
            json.dump(dictify(dicom), json_file, indent=4)    
    
def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting script with arguments: %s", args)
    if args.project.is_dir():
        _logger.info("The project is a directory")
        path_to_save = args.project.resolve() / "derivatives" / "png_slides"
        if args.level != 0:
            search_by_resolution_order(args.project, args.level, path_to_save)
        if args.chunk != 0:
            search_by_chunk(args.project, args.chunk, path_to_save)
    else:
        _logger.error("The project is not a directory")

    
        
        
    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m piramidaldcm2png.skeleton 42
    #
    run()
