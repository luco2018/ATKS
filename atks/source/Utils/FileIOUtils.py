#!/usr/intel/bin/python3.6.1

#  Copyright (C) 2018 Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause

"""Doc String Here"""

# Import built in modules
import os

# Import 3rd party modules

# Import local modules

# Module authorship metadata
__author__ = "Ryan Roberts"
__copyright__ = "Copyright 2018, Intel Corporation"
__credits__ = [""]
__license__ = "BSD-3-Clause"
__version__ = "1.0"
__maintainer__ = "Ryan Roberts, Erik W Berg"
__email__ = ""
__status__ = "Production"  # Prototype, Development, Production


def get_module_name_from_path(path):
    """

    :param path:
    :return:
    """
    filename = os.path.basename(path)
    return filename[:filename.rindex(".")]

def is_invalid_file_string(filename):
    """

    :param filename:
    :return:
    """
    return (type(filename) != str) or (filename == "")

def find_file_recursively(filename):
    """

    :param filename:
    :return:
    """
    findCmd = _create_find_cmd(filename)
    fileNames = os.popen(findCmd)
    shortest_file_path = _get_shortest_file_path(fileNames)
    fileNames.close()
    if shortest_file_path:
        return shortest_file_path
    else:
        raise FileNotFoundError("Unable to recursively find file: " + filename)

def is_file(filename):
    """
    Tests whether a file exists; will handle gzipped and non-gzipped files

    :param filename: string
    :return: bool
    """
    if filename.endswith('gz'):
        return (os.path.isfile(filename) or os.path.isfile(filename[:filename.rindex(".")])) and "~" not in filename and ".swp" not in filename
    return (os.path.isfile(filename) or os.path.isfile(filename+ ".gz")) and "~" not in filename and ".swp" not in filename

def _create_find_cmd(filename):
    """

    :param filename:
    :return:
    """
    (dir, base) = os.path.split(filename)
    return "find " + dir + " -name " + '"*' + base + '*"'

def _get_shortest_file_path(filenames):
    """

    :param filenames:
    :return:
    """
    realFiles = _get_real_files(filenames)
    return min(realFiles, key=len) if realFiles else None

def _get_real_files(filenames):
    """

    :param filenames:
    :return:
    """
    strippedFiles = [f.strip() for f in filenames if is_file(f.strip())]
    return strippedFiles
