#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""Base Project classes"""

# Import built in modules

# Import 3rd party modules

# Import local modules
from atks.source.Atks import Atks

from atks.source.AtksObject import AtksMeta
from atks.source.AtksObject import AtksObject

# Module authorship metadata
__author__ = "Ryan Roberts"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Ryan Roberts, Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production

class AtksProjectMeta(AtksMeta):
    """
    AtksProject Meta. This meta:
    1) automatically registers any defined projects with Atks.
    2) declares empty dictionary for the executables attribute on any project
    3) creates a unique project logger

    """
    def __new__(meta, cls_name, cls_supers, cls_dict):
        """
        Creates a logger for the class
        """
        atks = Atks()
        # Every project must have its own independent copy of executables
        cls_dict["executables"] = {}
        cls = super().__new__(meta,cls_name,cls_supers,cls_dict)
        cls.logger = cls._create_child_logger_for_class("Projects")
        if cls_name == "AtksProject": #we don't want to register the base class
            return cls
        atks.register_project(cls)
        return cls

class AtksProject(AtksObject, metaclass=AtksProjectMeta):
    """
    All Atks Projects must inherit from this class.
    """
    def __init__(self):
        super().__init__()
        self.executable_insts = []

    @classmethod
    def inherit_projects(cls):
        """

        Expected to be overwritten in a class extending from AtksProject.  Overwrite this method and call the
        'inherit_project' method with the handle to another imported AtksProject; serves to couple projects such
        that if A inherits B, B will always run when A is run

        :return: none
        """
        pass

    @classmethod
    def inherit_project(cls, proj):
        """

        :param proj: AtksProject class handle
        :return: none
        """
        cls.atks.mark_project_for_instantiation(proj)


    @classmethod
    def register_executable(cls, executable):
        """
        Registers an executable with the project.

        :param executable: AtksExecutable class handle
        :return: none
        """
        cls.executables[executable.__name__] = executable
        cls.logger.debug("Registered executable - " + executable.__name__)

    def configure(self):
        """
        Configures the project by setting up its executables

        :return: none
        """
        self._setup_executables()

    def _setup_executables(self):
        """
        Instantiates executables to set them up for execution

        Future improvement:  Add logic to limit the executables that will run (via the cmdline)

        :return: none
        """
        for executable in self.executables.values():
            self.executable_insts.append(executable())

    def execute(self):
        """
        Calls each instantiated AtksExecutable's 'execute' method

        :return: none
        """
        self.logger.info("Executing project")
        for executable in self.executable_insts:
            executable.execute()
        self.logger.info("DONE Executing project")

    def get_output(self):
        """
        Collects output from all instantiated AtksExecutable subclasses. If any output is
        received, prepends a header to the project.

        Future improvement:  Add detail to header; Add delimiter between output from different projects

        :return: string
        """
        header = "Output from Project " + self.__class__.__name__ + ": \n"
        output = ""
        for executable in self.executable_insts:
            output += executable.output
            output += "\n" if executable.output else ""

        self.output = header + output if output else ""

        return self.output






