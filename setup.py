#!/usr/bin/env python

import distutils.core
import sys

try:
    import setuptools
except ImportError:
    pass

version = "0.2"

with open('README.rst') as f:
    long_description = f.read()

distutils.core.setup(
    name="simple_vp",
    version=version,
    packages = ["simple_vp"],
    #package_data = {
    #    "simple_vp": ["adata.csv"],
    #    },
    author="Koteth",
    author_email="koteth@gmail.com",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Implementation of a vp-tree in pure python",
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        ],
    long_description=long_description,
)
