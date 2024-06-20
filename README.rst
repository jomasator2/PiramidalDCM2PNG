.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/PiramidalDCM2PNG.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/PiramidalDCM2PNG
    .. image:: https://readthedocs.org/projects/PiramidalDCM2PNG/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://PiramidalDCM2PNG.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/PiramidalDCM2PNG/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/PiramidalDCM2PNG
    .. image:: https://img.shields.io/pypi/v/PiramidalDCM2PNG.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/PiramidalDCM2PNG/
    .. image:: https://pepy.tech/badge/PiramidalDCM2PNG/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/PiramidalDCM2PNG
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/PiramidalDCM2PNG

    .. image:: https://img.shields.io/conda/vn/conda-forge/PiramidalDCM2PNG.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/PiramidalDCM2PNG
.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
.. image:: https://img.shields.io/coveralls/github/jomasator2/PiramidalDCM2PNG/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/jomasator2/PiramidalDCM2PNG

================
PiramidalDCM2PNG
================


Overview
--------

The `piramidaldicom2png` package is designed to convert one level of a pyramidal DICOM (Digital Imaging and Communications in Medicine) file into a group of PNG (Portable Network Graphics) images. This conversion is particularly useful in medical imaging where DICOM is the standard format. However, for certain applications like machine learning models or web visualization, PNG format might be more suitable due to its wide acceptance and smaller size.

The package provides a command-line interface (CLI) for easy conversion of these files. The CLI is installed as `fibonacci` in the current environment when the package is installed.

Installation
------------

To install the package, use pip:

.. code-block:: sh

    pip install piramidaldicom2png

Requirements
~~~~~~~~~~~~

Ensure you have the following dependencies installed:

- `dcm2mids==0.0.post1.dev87+g0177b14`
- `gdcm==1.1`
- `numpy==1.24.4`
- `pillow==10.3.0`
- `pydicom==2.4.4`
- `SimpleITK==2.3.1`

You can install these dependencies using pip:

.. code-block:: sh

    pip install dcm2mids==0.0.post1.dev87+g0177b14 gdcm==1.1 numpy==1.24.4 pillow==10.3.0 pydicom==2.4.4 SimpleITK==2.3.1

or 

.. code-block:: sh

    pip install -r requirements.txt

Usage
-----

Command-Line Interface (CLI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The CLI allows for easy conversion of DICOM files to PNG. The basic usage is as follows:

.. code-block:: sh

    piramidaldicom2png -p <path_to_project> -l <level> [--verbose] [--very-verbose]

- `-p`, `--project`: Path to the BIDS/MIDS project to convert.
- `-l`, `--level`: The level in the pyramidal DICOM to convert.
- `-v`, `--verbose`: Set loglevel to INFO.
- `-vv`, `--very-verbose`: Set loglevel to DEBUG.

Example
~~~~~~~

To convert a level in a pyramidal DICOM file to PNG images:

.. code-block:: sh

    piramidaldicom2png -p /path/to/project -l 2 --verbose

Python API
~~~~~~~~~~

The package also provides a Python API that can be used in scripts or interactive interpreters.

Example
~~~~~~~

.. code-block:: python

    from piramidaldcm2png import convert_dicom_to_png

    convert_dicom_to_png(project_path="/path/to/project", level=2, loglevel="INFO")

Development
-----------

Setting up for development
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository:

.. code-block:: sh

    git clone https://github.com/jomasator2/piramidaldicom2png.git
    cd piramidaldicom2png

2. Install the package in development mode:

.. code-block:: sh

    pip install -e .

Running Tests
~~~~~~~~~~~~~

To run tests, use pytest:

.. code-block:: sh

    pytest

License
-------

This project is licensed under the MIT License. See the `LICENSE` file for more details.

Author
------

- **jomasator2**

References
----------

- `Entry points <https://setuptools.pypa.io/en/latest/userguide/entry_point.html>`_
- `Pip installation <https://pip.pypa.io/en/stable/reference/pip_install>`_
- `dcm2mids <https://pypi.org/project/dcm2mids/>`_
- `gdcm <https://pypi.org/project/gdcm/>`_
- `numpy <https://pypi.org/project/numpy/>`_
- `pillow <https://pypi.org/project/Pillow/>`_
- `pydicom <https://pypi.org/project/pydicom/>`_
- `SimpleITK <https://pypi.org/project/SimpleITK/>`_
```