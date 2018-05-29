#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""
Base Atks objects. These should serve as the base for any object to inherit from.
"""

# Import built in modules
import logging

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

class AtksMeta(type):
    """

    """
    def __new__(meta, cls_name, supers, cls_dict):
        cls = type.__new__(meta, cls_name, supers, cls_dict)
        cls.logger = cls._create_child_logger_for_class("")
        return cls

    def _create_child_logger_for_class(cls, prefix):
        if hasattr(cls.atks, "logger"):
            return cls.atks.logger.getChild(prefix + "." + cls.__name__)
        else: #only expect to hit this in unit tests
            return logging.getLogger(cls.__module__)

class AtksObject(object, metaclass=AtksMeta):
    """
    Creates a pointer
    """
    atks = Atks()
    def configure(self):
        """
        Object configures itself - instantiates child objects, sets attributes, etc

        :return: none
        """
        pass
