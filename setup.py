from setuptools import setup, find_packages
import numpy

setup(
    name="lecroy_control", packages=find_packages(), include_dirs=[numpy.get_include()]
)
