# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

from setuptools import setup, Extension, find_packages
import sys


setup(name='ATKS',
      version='1.0',
      description='',
      author='Erik Berg',
      author_email='',
      url='',
      packages=find_packages(),
      python_requires=">=3.6.1",
      install_requires = [],
      entry_points = { 'console_scripts' : [
            'atks = atks.main:main'
      ],

      },
      )
