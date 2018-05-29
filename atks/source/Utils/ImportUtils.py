#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""This library contains a set of utility functions to simplify imports."""

# Import built in modules
import pkgutil, sys

# Import 3rd party modules

# Import local modules

# Module authorship metadata
__author__ = "Ryan Roberts"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Ryan Roberts, Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production

# Code starts here

def import_modules_from_path(paths):
    """
    Imports all modules and packages from the list of paths given. Will not import a module
    if it has already been imported

    :param paths: list of paths (represented as strings) to import the modules from
    :return:
    """

    sys.path.extend(paths)
    for loader, module_name, ispkg in pkgutil.walk_packages(paths):
        if (not module_name in sys.modules): #make sure we don't double import a module
            loader.find_module(module_name).load_module(module_name)


