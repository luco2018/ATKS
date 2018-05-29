#!/usr/intel/bin/python3.6.1

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import logging
import os
import sys
import unittest
import argparse

from atks.source.Atks import Atks

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.atks = Atks()
        self.configure_atks_for_testing()
        self.atks.setup_projects()

    def tearDown(self):
        self.atks.out_file.close()

    def assert_project_registered(self, project):
        self.assertIn(project, self.atks.registered_projects)

    def assert_project_not_registered(self,project):
        self.assertNotIn(project, self.atks.registered_projects)

    def assert_project_instantiated(self, project):
        instantiated_projects = [inst.__class__.__name__ for inst in self.atks.proj_insts]
        self.assertIn(project, instantiated_projects)

    def assert_executable_registered_in_project(self, project, executable):
        self.assertIn(executable, self.atks.registered_projects[project].executables)

    def assert_executable_not_registered_in_project(self, project, executable):
        self.assertNotIn(executable, self.atks.registered_projects[project].executables)

    def assert_object_has_attribute_of_type(self, object, attrname, attrtype):
        self.assertTrue(hasattr(object,attrname))
        self.assertTrue(type(getattr(object,attrname)) is attrtype)

    def get_project_inst(self, project):
        return [proj for proj in self.atks.proj_insts if proj.__class__.__name__ == project][0]

    def get_executable_inst_from_project(self, project, executable):
        return [exe for proj in self.atks.proj_insts for exe in proj.executable_insts  if proj.__class__.__name__ == project if exe.__class__.__name__ == executable][0]

    def assert_has_logger(self, object):
        self.assert_object_has_attribute_of_type(object, "logger", logging.Logger)

    def assert_output_propogates_up(self, fromObj, toObj):
        self.assertIn(fromObj.output, toObj.output)

    def create_args_namespace(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config')
        parser.add_argument('--proj')
        return parser.parse_args(['--config', 'TestAtksConfig.py'])

    def configure_atks_for_testing(self):
        self.atks.args = self.create_args_namespace()
        self.atks.configure()
        self.atks.setup_projects()
        self.atks.out_file = open("/dev/null", "w")
        self.atks.log_out_file = sys.stdout
        self.atks._configure_logging()

        #self.atks.logger.setLevel(logging.DEBUG)
        #self.atks.project_areas = [os.path.join(os.getcwd(), "tests/integration_tests/Projects/ProjectA")]
        pass

    def test_atks_integration_project_registered(self):
        self.assert_project_registered("ProjectA")
        self.assert_project_registered("ProjectB")
        self.assert_project_not_registered("ProjectC")

        self.assert_project_instantiated("ProjectA")
        self.assert_project_instantiated("ProjectB")

    def test_atks_integration_executable_registered(self):
        self.assert_executable_registered_in_project("ProjectA", "Script1")
        self.assert_executable_registered_in_project("ProjectA", "Script2")
        self.assert_executable_registered_in_project("ProjectB", "Script1")
        self.assert_executable_registered_in_project("ProjectB", "Script3")
        self.assert_executable_not_registered_in_project("ProjectB", "Script2")

    def test_atks_integration_has_logger(self):
        self.assert_has_logger(self.get_project_inst("ProjectA"))
        self.assert_has_logger(self.get_project_inst("ProjectB"))
        self.assert_has_logger(self.get_executable_inst_from_project("ProjectA", "Script1"))
        self.assert_has_logger(self.get_executable_inst_from_project("ProjectA", "Script2"))
        self.assert_has_logger(self.get_executable_inst_from_project("ProjectB", "Script1"))
        self.assert_has_logger(self.get_executable_inst_from_project("ProjectB", "Script3"))

    def test_atks_integration_run_output(self):
        self.atks.run()
        self.assert_output_propogates_up(self.get_executable_inst_from_project("ProjectA", "Script1"), self.get_project_inst("ProjectA"))
        self.assert_output_propogates_up(self.get_executable_inst_from_project("ProjectB", "Script3"), self.get_project_inst("ProjectB"))
        self.assert_output_propogates_up(self.get_project_inst("ProjectA"), self.atks)




if __name__ == '__main__':
    unittest.main()
