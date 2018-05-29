#!/usr/intel/bin/python3.6.1

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import unittest

from atks.source.Atks import Atks

from atks.source.Project.AtksProject import AtksProject

class test_AtksProject(unittest.TestCase):
    def setUp(self):
        self.atks = Atks()


    def test_no_registered_projects(self):
        self.assertEqual(self.atks.registered_projects, {})

    def test_projects_get_registered(self):
        class projA(AtksProject):
            pass

        class projB(AtksProject):
            pass
        self.assertEqual(self.atks.registered_projects, {"projA": projA, "projB": projB})


if __name__ == '__main__':
    unittest.main()