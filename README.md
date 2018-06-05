Copyright (C) 2018 Intel Corporation  
SPDX-License-Identifier: BSD-3-Clause

Automation Through Knowledge Sharing (ATKS)
------------
[Package description](#package-description)  
[ATKS components](#atks-components)

Package description
----------------------

ATKS and [ThenWhatTree](https://github.com/intel/ThenWhatTree) were developed to solve a simple problem: debug information was tribal, poorly communicated and globally distributed.  The two packages are standalone but together define a formalism for platform-agnostic, extensible debug scripting.  While we encourage teams to use the ThenWhatTree package to define executables, the VASE platform can run any python modules that users choose.  This README contains examples based on ThenWhatTree executables.  


Block diagram
---------
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



ATKS components
--------
Prior to running ATKS, you will need to create the projects and executables that ATKS will consume.

[Projects](#projects)<br>
[Executables](#executables)<br>
[ThenWhatTree_libs](#thenwhattree_libs)
[Plugins](#plugins)<br>

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

The executables directory contains an empty \_\_init__.py file and any scripts available to be run.  ATKS expects an executable to return a string.  There are no constraints on the name of a project, however, the name should be unique to avoid aliasing with executables from other ATKS projects.
<pre>
> ls Executables/
__init__.py  my_flow.py
</pre>

my_flow.py
---
Example source code is below.  There are no constraints on the name of the class.  Whatever name is given will be used to identify the tree output in atks.log.
<pre>
#!/usr/bin/env/python3.6.1
"""Project description here"""<br>
import AtksExecutableTWT
from my_project import my_project<br>

class my_flow(AtksExecutableTWT, Project = my_project, xml_path = \<path to XML file with ThenWhatTree nodes>):
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

class my_flow(AtksExecutableTWT, Project = my_project, xml_path = \<path to XML file with ThenWhatTree nodes>):
    pass
</pre>
</ol>  

[[twt|ThenWhatTree/blob/master/README.md#example-input-and-output]]
Sample output  
---
The output from the executable will be under the name of the class ('my_flow' in this example) in the atks.log file.
<pre>
Output from Project my_project: 
Output from Executable my_flow:  <---------------------------- 
[0] Rootnode : true
    [1] Subnode1 : true
        [2] Subnode11 : true
        Subnode12 : NotImplementedError
        Subnode13 : ZeroDivisionError('division by zero',)
    Subnode2 : false
    Subnode3 : NotImplementedError
</pre>

ThenWhatTree_libs
---
Directions on how to create decision tree libraries for executables can be found on the [ThenWhatTree](https://github.com/intel/ThenWhatTree) page.  There are no constraints on the name of this directory.
<pre>
> ls ThenWhatTree_libs
my_flow
</pre>
The my_flow library is where the XML and python modules for that tree live.
<pre>
> ls my_flow
Rootnode.py     Subnode11.py      Subnode13.py      Subnode31.py
Rootnode.xml    Subnode32.py      Subnode111.py     Subnode2.py
Rootnode.xml    Subnode1.py       Subnode12.py      Subnode3.py
</pre>


Plugins
---
FIXME

AtksConfig.py
---
The default is to run the AtksConfig in the atks repo. This can be overridden on the cmd line with the --config switch.  A AtksConfig.py template is shown.  In the current example, 'my_project' would be added to the 'project_areas' list.

<pre>
config = {
    "project_areas": ['<local_project_path_1>', '<local_project_path_2>'],
    "out_file": "atks.log",
    "log_out_file": "atks_report.log",
    "disable_plugins": [],
}</pre>

Command line
----
No --config required; project paths are taken from the AtksConfig in the atks repo.
<pre>
> atks
</pre>

Output file: atks.log
----
The output file name can be configured in the AtksConfig

The hints from all scripts are collected into the atks/atks.log file in your run directory.  Example output from the decision tree created for my_flow is shown below.  Features of the report include:
  * The name of the project
  * The name of the executable
  * Annotation of the tree showing the results of the walk and the index of the hint for each node returning 'True'
  * Annotation of the decision tree showing nodes that raised exceptions
  * Indexed list of all hints that were found
  * List of the node raising exceptions with type
  * List of the traceback for each exception
  
The example below is from our internal testing.  The intent is to show the structure and content of atks.log.  
<pre>
Output from Project my_project: 
Output from Executable my_flow: 
[0] Rootnode : true
    [1] Subnode1 : true
        [2] Subnode11 : true
        Subnode12 : NotImplementedError
        Subnode13 : ZeroDivisionError('division by zero',)
    Subnode2 : false
    Subnode3 : NotImplementedError
<br>

Node output:
\------------
[0] Rootnode is true
[1] Subnode1 is true
[2] Subnode11 is true

Exceptions:
\-----------
Subnode12: NotImplementedError
Subnode13: ZeroDivisionError('division by zero',)
Subnode3: NotImplementedError

Exception traceback:
\--------------------
Subnode13: ['  File "ThenWhatTree/lib/twt_node/ThenWhatTreeNode.py", line 67, in evaluate_node_is_true\n    node_is_true = str(self.is_true()).lower()\n', '  File "ThenWhatTree_libs/my_flow/Subnode13.py", line 14, in is_true\n    return 1/0\n']
</pre>
