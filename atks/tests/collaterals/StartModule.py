#!/usr/intel/bin/python3.6.1

# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause


import os,sys
from DataClass import DataClass,decoratorScenario

class MyClass(DataClass):
       
    @decoratorScenario
    def ScenarioRegister(self, *args):
        self.scenario = args[0][0]
        return self    



