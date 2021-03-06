#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""This module parses command line arguments, instantiates Atks and calls the atks main flow"""

# Import built in modules
import argparse
import os

# Import 3rd party modules

# Import local modules
from atks.source.Atks import Atks

# Module authorship metadata
__author__ = "Ryan Roberts"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Ryan Roberts, Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proj", help="specifies project to run")
    parser.add_argument("--config", help="specifies a path to a atks_config file to use for configuration")
    return parser.parse_args()

def main():
    args = _parse_arguments()
    atks = Atks()
    atks.args = args
    atks.configure()
    atks.integrate_plugins()
    atks.setup_projects()
    atks.pre_run()
    atks.run()
    atks.postprocess()
    atks.cleanup()



if __name__ == "__main__":
    os.environ['PYTHONDONTWRITEBYTECODE'] = 'TRUE'
    main()
