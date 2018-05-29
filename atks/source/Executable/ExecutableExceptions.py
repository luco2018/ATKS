#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""
Executable Exceptions file. Exceptions raised by executables should be defined in this file.
"""

# Import built in modules

# Import 3rd party modules

# Import local modules
from atks.source.Exceptions import AtksError

# Module authorship metadata
__author__ = "Ryan Roberts"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Ryan Roberts, Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production


class ExecutableError(AtksError):
    """
    All Executable Errors should extend from this class
    """
    pass

class InvalidProjectError(ExecutableError):
    """
    Raised when a bad project is passed to the class definition of an executable
    """
    pass
