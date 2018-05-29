#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""
Base Atks Exceptions.
"""

# Import built in modules

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

class AtksError(Exception):
    """ Base Exception for Atks. All exceptions should extend from this exception."""
    pass

class ProjectRegistrationError(AtksError):
    """ Raised whenever a project fails to register"""
    pass

class ProjectInstantiationError(AtksError):
    """Raised whenever a project cannot be instantiated"""
    pass