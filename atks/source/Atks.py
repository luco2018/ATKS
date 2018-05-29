#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""
Atks object which serves as the main executor of the project.
Atks import and integrates plugins, registers and executes the projects, collects the output, and outputs said output.
"""

# Import built in modules
import logging
import sys
from types import ModuleType
import importlib.machinery
import pkgutil

# Import 3rd party modules

# Import local modules
import atks.source.Utils.ImportUtils as ImportUtils
from atks.source.Utils.FileIOUtils import get_module_name_from_path
from atks.source.Exceptions import ProjectRegistrationError, ProjectInstantiationError

# Module authorship metadata
__author__ = "Ryan Roberts"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Ryan Roberts, Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production


class Atks(object):

    singleton_inst = None

    def __new__(cls, *args, **kwargs):
        if not cls.singleton_inst:
            cls.singleton_inst = super().__new__(cls,*args,**kwargs)
            cls.singleton_inst.initialized = False
        return cls.singleton_inst

    def __init__(self):
        if self.initialized:
            return
        self.projects_to_instantiate = set()
        self.registered_projects = {}
        self.integrated_plugins = {}
        self.proj_insts = []
        self.project_areas = []
        self.initialized = True
        self.log_out_file = sys.stdout
        self.out_file = sys.stdout
        self.disable_plugins = []
        self.args = None


    def configure(self):
        """
        Configures atks.
        Reads the config dictionary and initializes the logging module.
        :return: none
        """
        if self.args.config:
            module_name = get_module_name_from_path(self.args.config)
            module = importlib.machinery.SourceFileLoader(module_name, self.args.config).load_module()
            config = module.config
        else:
            from atks.config.AtksConfig import config
        self.__dict__.update(config)
        self._configure_logging()

    def _configure_logging(self):
        """
        Initializes the logging module.
        Sets a base logger, formats it, and adds a handler to direct the output to the desired file.

        :return: none
        """

        self.logger = logging.getLogger("Atks")
        if type(self.log_out_file) is str :
            handler = logging.FileHandler(self.log_out_file,mode="w")
        else:
            handler = logging.StreamHandler(self.log_out_file)
        formatter = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)







    def integrate_plugins(self):
        """
        Imports all the plugins which are registered as 'entry_points' in setup.py
        Plugins should be imported by the individual consumers of them. They will be accessible under AtksPlugins.<plugin_name>
        """

        try:
            import AtksPlugins
        except:
            pass
        else:
            for loader, module_name, ispkg in pkgutil.iter_modules(AtksPlugins.__path__):
                if module_name not in self.disable_plugins:
                    plugin = loader.find_module(module_name).load_module(module_name)
                    self.logger.debug("Imported plugin - " + module_name)
                    if hasattr(plugin, "integrate"):
                        plugin.integrate(self)
                        self.logger.debug("Integrated plugin - " + module_name + " with integrate method")
                    else:
                        self.logger.debug("Integrated plugin - " + module_name + " without integration method")


    def register_project(self, proj):
        """
        Registers a project with Atks.  Raises a ProjectRegistrationError if registration fails.

        :param proj: AtksProject object
        :return: none
        """

        if proj.__name__ in self.registered_projects and proj is not self.registered_projects[proj.__name__]:
            raise ProjectRegistrationError("Project: " + proj.__name__ + " could not be registered because another project by the same name has already been registered.")
        self.registered_projects[proj.__name__] = proj
        self.logger.debug("Registered project - " + proj.__name__)

    def mark_project_for_instantiation(self, proj):
        """
        marks the input project for instantiation. Only projects marked for instantiation will be insantiated and ran.

        :param proj: AtksProject object
        :return: none
        """
        self.logger.debug("Marking project: " + proj.__name__ + " for instantiation")
        self.projects_to_instantiate.add(proj)

    def _mark_initial_project_for_instantiation(self):
        """
        Looks at the proj argument passed to atks and marks it for instantiation. If no proj argument is given, all projects are marked for instantiation.

        :return: none
        """
        if self.args.proj is None:
            for proj_name in self.registered_projects:
                self.mark_project_for_instantiation(self.registered_projects[proj_name])

        else:
            if self.args.proj not in self.registered_projects :
                raise ProjectInstantiationError("Project " + str(self.args.proj) + " specified on command line cannot be instantiated because no project is registered under that name")
            self.mark_project_for_instantiation(self.registered_projects[self.args.proj])

    def _import_projects(self):
        """
        Imports all Atks projects.

        :return: none
        """

        self.logger.debug("Importing all modules from paths " + ",".join(self.project_areas))
        ImportUtils.import_modules_from_path(self.project_areas)

    def _determine_projects_to_instantiate(self):
        """
        Marks initial project for instantiation and iterates

        :return: none
        """
        projects = None
        self._mark_initial_project_for_instantiation()

        while projects != list(self.projects_to_instantiate):
            projects = list(self.projects_to_instantiate)
            for proj in projects:
                proj.inherit_projects()


    def _create_projects(self):
        """
        Instantiates all imported Atks projects and appends them to an attribute of project instances.

        :return: none
        """
        for proj in self.projects_to_instantiate:
            self.proj_insts.append(proj())

    def _configure_projects(self):
        """
        Calls the configure method on all instantiated projects

        :return: none
        """
        for proj in self.proj_insts:
            proj.configure()

    def _execute_projects(self):
        """
        Executes all instantiated projects by calling its execute method.

        :return: none
        """
        for proj in self.proj_insts:
            proj.execute()

    def _get_output_from_projects(self):
        """
        Gets each project's output and concatenates it together.

        :return: none
        """
        output = ""
        for proj in self.proj_insts:
            output += proj.get_output()

        self.output = output
        return output

    def _print_output(self, output):
        """
        Takes some output and prints it to the configured output file.
        args: Output - a string of output to print

        :return: none
        """
        if type(self.out_file) is str:
            with open(self.out_file, "w") as f:
                print(output, file=f)
        else:
            print(output, file = self.out_file)

    def setup_projects(self):
        """
        Calls all methods needed to setup projects

        :return: none
        """
        self._import_projects()
        self._determine_projects_to_instantiate()
        self._create_projects()
        self._configure_projects()

    def pre_run(self):
        """
        Filler task created to allow plugins to preprocess if they need to

        :return:
        """
        pass

    def run(self):
        """
        Executes all projects, gets their output, and prints it

        :return: none
        """
        self._execute_projects()
        output = self._get_output_from_projects()
        self._print_output(output)

    def cleanup(self):
        """
        Filler task created to allow plugins to postprocess if they need to

        :return: none
        """
        pass

    def postprocess(self):
        """
        Placeholder method

        :return:
        """
        pass