#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""Doc String Here"""

# Import built in modules

# Import 3rd party modules

# Import local modules
from atks.source.Executable.AtksExecutable import AtksExecutable
from ..ProjectB import ProjectB

# Module authorship metadata
__author__ = "Ryan Roberts"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Ryan Roberts, Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production


class Script1(AtksExecutable, Project = ProjectB):
    def execute(self):
        self.output = "Script 1 hint"
