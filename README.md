Copyright (C) 2018 Intel Corporation  
SPDX-License-Identifier: BSD-3-Clause

Automation Through Knowledge Sharing (ATKS)
------------
ATKS and [ThenWhatTree](https://github.com/intel/ThenWhatTree) were developed to solve a simple problem: debug information was tribal, poorly communicated and globally distributed.  Used in concert the two packages provide an efficient framework to distill the knowledge of debug experts into recipes that can be easily shared and studied for additional insights.  The two packages are standalone but together define a formalism for platform-agnostic, extensible debug scripting and expert knowledge sharing.  

In 2012, Dr. Atul Gawande wrote an [article](https://www.newyorker.com/magazine/2012/08/13/big-med) where he marveled at the efficiency of the Cheesecake Factory and looked for insights to improve the healthcare system.  During an interview on a Freakonomics podcast, he summarized the approach of one restaurant manager thusly, "I would look to see what the best people are doing, I would find a way to turn that into a recipe, make sure everyone else is doing it and see how far we improve and try learning again from that."  Healthcare, restaurants and debug seem disparate but all can be treated as a supply chain problem.  ATKS and [ThenWhatTree](https://github.com/intel/ThenWhatTree) start from the premise that most debug knowledge already exists and does not require discovery.  These packages create a means to efficiently capture and connect dispersed debug knowledge with any test failure where it is relevant.


[Getting started](#getting-started)  
[Package description](#package-description)  
[ATKS components](#atks-components)  
 * [Block diagram](#block-diagram)
 * [Projects](#projects)
 * [Executables](#executables)
 * [Plugins](#plugins)
 * [Config](#config)


Getting started
---
FIXME 

Command line
----
No --config required; project paths are taken from the AtksConfig in the atks repo.
<pre>
> atks
</pre>

ATKS components
--------
Prior to running ATKS, you will need to create the projects and executables that ATKS will consume.  Plugins are not required but allow the opportunity for sharing best practices for data extraction.

Block diagram
---------
The various components of the ATKS framework are shown below.  
<pre>
                               +----------+      +----------+      +----------+
                               |          |      |          |      |          |
                               | Plugin_1 |      | Plugin_2 |      | Plugin_3 |
                               |          |      |          |      |          |
                               +------^---+      +-------^--+      +--------^-+
                                      |                  |                  |
                                      |                  |                  |
                               +------+------------------+------------------+-----+
                               |                                                  |
                               |                       ATKS                       |
                               |                                                  |
                               +--+----------------------+----------------------+-+
                                  |                      |                      |
                                  |                      |                      |
                                  |                      |                      |
                        +---------v-+             +------v----+             +---v-------+
                        |           |             |           |             |           |
                        | Project_A |             | Project_B |             | Project_C |
+--------------+        |           |             |           |             |           |
|              <--------+-+-------+-+             +------+----+             +---+---+---+
| Executable_1 |          |       |                      |                      |   |
|              |          |       |                      |                      |   |
+--------------+          |       |                      |                      |   |  +--------------+
                          |       |             +--------v-----+                |   +-->              |
            +-------------v+      |             |              |                |      | Executable_6 |
            |              |      |             | Executable_4 |                |      |              |
            | Executable_2 |      |             |              |      +---------v----+ +--------------+
            |              |      |             +--------------+      |              |
            +--------------+      |                                   | Executable_5 |
                                  |                                   |              |
                          +-------v------+                            +--------------+
                          |              |
                          | Executable_3 |
                          |              |
                          +--------------+
</pre>

Projects
---
All ATKS projects extend from the AtksProject class.  A project is a collection of executables.  

my_project.py
---
The sole purpose of this file is to create a class extension of the AtksProject object with the project name.  There are no constraints on the name of this file.
<pre>
> cat my_project.py<br>

#!/usr/bin/env/python3
"""Project description here"""<br>
\# Import local modules
from atks import AtksProject<br>
\# Code starts here<br>
class my_project(AtksProject):
&nbsp;   pass
</pre>

Executables
---
All ATKS executables extend from the AtksExecutable class.  An executable must import the project to which it belongs.<br>

While we encourage teams to use the [ThenWhatTree](https://github.com/intel/ThenWhatTree) package to define executables, the VASE platform can run any python modules that users choose.  The example below is based on ThenWhatTree executables.  

The executables directory contains an empty \_\_init__.py file and any scripts available to be run.  ATKS expects an executable to return a string.  There are no constraints on the name of a project, however, the name should be unique to avoid aliasing with executables from other ATKS projects.
<pre>
> ls Executables/
__init__.py  my_executable.py
</pre>

my_executable.py
---
Example source code for an executable built from a [ThenWhatTree](https://github.com/intel/ThenWhatTree) is below.  There are no constraints on the name of the class.  Whatever name is given will be used to identify the tree output in atks.log.
<pre>
#!/usr/bin/env/python3.6.1
"""Project description here"""<br>
import AtksExecutableTWT
from my_project import my_project<br>

class my_executable(AtksExecutableTWT, Project = my_project, xml_path = \<path to XML file with ThenWhatTree nodes>):
&nbsp;   pass
</pre>
There are two sections that need to be updated for each specific executable.
<ol>
<b><li>Imports</li></b>
The project must be imported so that it can be passed as part of the class declaration.
<pre>
import AtksExecutableTWT
from my_project import my_project
</pre>
<b><li>Class definition</li></b>
A class must be defined that contains an 'execute' method.  When using the ThenWhatTree package to define executable collateral, the class definition looks like this.  The xml_path is specific to this example and directory structure.  It is only required to be a full path to a XML file inside a ThenWhatTree library of python modules.  The default behavior is for the class to do nothing and pass.
<pre>

class my_executable(AtksExecutableTWT, Project = my_project, xml_path = \<path to XML file with ThenWhatTree nodes>):
    pass
</pre>
</ol>  

Sample input and output from ThenWhatTree executables can be found [here](https://github.com/intel/ThenWhatTree/blob/master/README.md#example-input-and-output)


Plugins
---
In the [ThenWhatTree](https://github.com/intel/ThenWhatTree/blob/master/README.md#thenwhattree-methodology) methodology, the debug flow and the data extraction to feed the debug flow are explicitly segregated.  Data extraction methods are created and shared in the plugins.  Examples of plugins include parsers for custom text files and signal trace files.  Expert knowledge about how to identify and extract event information is captured and shared through the plugins.

A plugin can be as simple as a function library or a plugin can run custom code during the registration with ATKS.  Any custom code that needs to run must be defined in a method called 'integrate' in the plugin's top level \_\_init__.py file.  

Config
---
The default is to run the AtksConfig in the atks repo. This can be overridden on the cmd line with the --config switch.  A AtksConfig.py template is shown.  In the current example, 'my_project' would be added to the 'project_areas' list.

<pre>
config = {
    "project_areas": ['<local_project_path_1>', '<local_project_path_2>'],
    "out_file": "atks.log",
    "log_out_file": "atks_report.log",
    "disable_plugins": [],
}</pre>


Output file: atks.log
----
The output file name can be configured in the AtksConfig

The hints from all scripts are collected into the atks/atks.log file in your run directory.  Example output from the decision tree created for my_flow is shown below.  Features of the report include:
  * The name of the project
  * The name of the executable
  * String returned from executable
  
The example below is from an ATKS that has the following components:  

Project:  
&nbsp;    my_project_A  
Executables registered with my_project_A:  
&nbsp;    my_executable_A1  
&nbsp;    my_executable_A2  
&nbsp;    my_executable_A3

Project:  
&nbsp;    my_project_B  
Executables registered with my_project_B:  
&nbsp;    my_executable_B1

The structure and content of atks.log is shown below.  
<pre>
Output from Project my_project_A:
Output from Executable my_executable_A1:
<i>"String returned from my_executable_A1"</i><br>
Output from Project my_project_A:
Output from Executable my_executable_A2:
<i>"String returned from my_executable_A2"</i><br>
Output from Project my_project_A:
Output from Executable my_executable_A3:
<i>"String returned from my_executable_A2"</i><br>
Output from Project my_project_B:
Output from Executable my_executable_B1:
<i>"String returned from my_executable_B1"</i><br>
</pre>
