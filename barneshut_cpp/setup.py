from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(ext_modules=cythonize(
    'cppsim_source/cppsim.pyx',
    language_level=3
), include_dirs=[numpy.get_include(), './'])