#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""
Base Executable Classes
"""

# Import built in modules

# Import 3rd party modules

# Import local modules
from atks.source.Executable.ExecutableExceptions import InvalidProjectError
from atks.source.AtksObject import AtksMeta
from atks.source.AtksObject import AtksObject

from atks.source.Project.AtksProject import AtksProject

# Module authorship metadata
__author__ = "Ryan Roberts"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Ryan Roberts, Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production

class AtksExecutableMeta(AtksMeta):
    """
    AtksExecutable meta:
    1) Adds a required project kwarg to all executables.
        --> kwarg assigns an executable to a project
    2) Validates that the project is a subclass of AtksProject
    3) Creates a logger

    """
    def __new__(meta, cls_name, cls_supers, cls_dict, *, Project = None):
        """
        Creates a class after registering it with the specified Project.
        Creates a logger for the class

        args: Project - AtksProject Class with which to register the executable.
        """
        cls = super().__new__(meta,cls_name,cls_supers,cls_dict)
        if "AtksExecutable" in cls_name: #we don't want to register the base class
            return cls
        if not Project:
            raise InvalidProjectError("Must specify a project in an executable class declaration with Project = <project>")
        if not issubclass(Project, AtksProject):
            raise InvalidProjectError("Project must inherit from AtksProject")
        cls.project = Project
        cls.logger = cls._create_child_logger_for_class("Projects." + Project.__name__ + ".Executables")
        Project.register_executable(cls)
        return cls

class AtksExecutable(AtksObject, metaclass= AtksExecutableMeta):
    """Base class for all executables. Every executable must inherit from this class."""

    def __init__(self):
        super().__init__()
        self._output = ""

    def execute(self):
        """
        This method gets called by the project to which the executable is assigned. Every executable
        should override this method.  Any output should be captured by assigning the 'output' attribute
        """
        pass

    @property
    def output(self):
        """
        This property gets passed up to the project. If some output returned, a header will be prepended.
        """
        header = "Output from Executable " + self.__class__.__name__ + ": \n"
        header += "-" * len(header) + "\n"
        return  header + self._output if self._output else ""

    @output.setter
    def output(self, message):
        self._output = message
