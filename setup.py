from distutils.core import setup
from Cython.Build import cythonize

import numpy

setup(
    ext_modules = cythonize("sandpile_inner.pyx"),
    include_dirs=[numpy.get_include()]
)
