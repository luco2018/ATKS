#!/usr/intel/bin/python3.6.1

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import unittest

from atks.source.Executable.ExecutableExceptions import InvalidProjectError
from atks.source.Executable.AtksExecutable import AtksExecutable

from atks.source.Project.AtksProject import AtksProject


class test_AtksProject(unittest.TestCase):
    def setUp(self):
        self.proj = AtksProject()

    def test_no_registered_projects(self):
        self.assertEqual(self.proj.executables, {})

    def test_projects_get_registered(self):
        class exeA(AtksExecutable, Project = AtksProject):
            pass

        class exeB(AtksExecutable, Project = AtksProject):
            pass
        self.assertEqual(self.proj.executables, {"exeA": exeA, "exeB": exeB})

    def test_raises_exception(self):
        with self.assertRaises(InvalidProjectError):
            class exeA(AtksExecutable): pass

        with self.assertRaises(InvalidProjectError):
            class exeA(AtksExecutable, Project = object): pass


if __name__ == '__main__':
    unittest.main()