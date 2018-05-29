#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""
Configuration file for Atks. Should contain a single dictionary named config with the following fields:

project_areas => list of paths in which to search for Atks Projects
out_file => output file for ATKS. Can be a string or sys.stdout
log_out_file =>  output file for ATKS logging. Can be a string or sys.stdout
disable_plugins => list of plugins which should be disabled when ATKS executed. Disabled plugins will not be imported or integrated.
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


# project_areas must be populated; if it's an empty list, then no projects will be registered

config = {
    "project_areas": [],
    "out_file": "atks.log",
    "log_out_file": "atks_report.log",
    "disable_plugins": [],
}
