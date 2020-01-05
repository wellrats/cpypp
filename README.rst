
Welcome to GitHub repository of cpypp 
=====================================

**cpypp** is the implementation of a c-stype preprocessor for Python Programming Languages 2.7+

A preprocessor is a program that takes a input Source Code written using some
programming language syntax and outputs an output Source Code that translate,
expand or modify original programming language.

For example, from this:

.. code:: python

    from cpypp import py_preprocessor
    PYPP = py_preprocessor()
    PYPP.parse(__file__, __name__)

    """This source will work in both Python versions"""

    def main():

       #ifdef __PYTHON2__
       #expand print "This will work in", "Python 2", "like a charm"
       #else
       print("This will work in Python 3 like a charm")
       #endif

    if __name__ == "__main__": main()

to this if we are using Python 3+

.. code:: python

    """This source will work in both Python versions"""

    def main():

       print("This will work in Python 3 like a charm")

    if __name__ == "__main__": main()

Table of Contents
=================

.. contents::

Introduction
============

I love to write code, and I love to keep my code clean and organized, specially when
I publish it on github for example. I love to use the latest features of a
language and I specially love debug with ``print`` and a lot of dashes  ``'-'`` and so on.

But, when you write open source code, a lot of ``prints``, ``dashes`` and latest features
are not welcome. Your code has to install and run in as many Python versions and platforms it it cans, and 
be kept up to date, stable and without bugs. Python 2.7 support is dropped since January 2020, 
but far away from be replaced. There is a lot of stuff that keeps working on it and still 
will be for a long time.  Why? Because the cost of conversion is expensive, needs
time and effort. And all this code has to be mantained, keep evolving and will need packages 
updates that be compatible with then and, when they began their conversion process, it will not be at once.

So this was the motivation to get the best of both worlds (thank you for Hanna Montanna). 
Create a preprocessor for Python language that could keep final code clean, stable, runnable in 
any version of Python, working at run time, or used as a command line tool for batch conversion.

Installing
----------

**cpypp** can be easily installed via common Python package managers such as pip.

::

    $ pip install cpypp

You may also get the latest **cpypp** version by grabbing the source code from Github:

::

    $ git clone https://github.com/wellrats/cpypp
    $ cd cpypp
    $ python setup.py install

To test your installation, cpypp come with a set of simple tutorials that can be executed once you 
have deployed the packages

::

    python -m cpypp.tests.test_helloworld

or

::

    python3 -m cpypp.tests.test_helloworld

Examples
--------

cpypp comes with some examples to check it out go to cpypp install directory

::

    $ cd $(dirname $(python -c "import cpypp; print(cpypp.__file__)"))
    $ python tests/py2andpy3.py
    $ python -m cpypp py2andpy3.py -o -
    $ python -m cpypp py2andpy3.py -r -o -

Runtime or command line processor?
==================================

Usually a preprocessor do its job at compile time, but Python don't have this feature 
so, pypy has two options do its job: at run time, when you are executing a source file as
a script or as a import module, or using a command line tool. Which to choose is up to you
and your motivations to use a preprocessor. Let's see the diferences between then.

Runtime preprocessor
--------------------

RunTime preprocessor is when you have the source code and wants to execute this code respecting the 
preprocessor directives. Probably you are a developer and want to insert some tests or let the code be prepared
to future releases of Python, but don't want this ``test code`` in your final code on GitHub or in you client, or
wants be able to generate many diferent codes from this one. 
This source code can be executed as a script calling ``python yourscript.py`` or loaded as a module using import 
``import your_module``. Like was written before, Python does not implements a preprocessor feature at compile time, so cpypp will simulate it at run time.  

But how can we do it at runtime? How can we modify a code that is compiled and running? The answer is
obvious: We can't. We can rewrite the code and executs it again, inside itself. In other words, we will execute
the source code twice. The first version is the original version where directives are seen as comments
by compiler. This code will be compiled and executed normally. During this execution when the 
``PYPP.parse( ...`` code is executed,  the trick happens. All code is read again, preprocessed 
and directives do their job and a brand new code is created. This new code is executed and takes place 
of original code.  

There's a little difference if original code is executed as a script or is being imported. 
When the variable ``__name__`` has the value ``"__main__"``, cpypp assumes this is a script and not an
import module. The differences are bellow:

How Python and cpypp works when source code is a script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First let's see a graphical flow how Python and cpypp will do their job to guarantee that the preprocessor will work
properly when running a script.

::

    Flow
    |
    1️⃣ Python reads original .py script file
    2️⃣ compiles it in memory (.pyc)
    3️⃣ runs the compiled code
       |
       1️⃣ All code before "PYPP.parse( ..." is executed ✅✅
       2️⃣ When "PYPP.parse( ..." is called
       |  |
       |  1️⃣ PYPP reads original .py file
       |  2️⃣ parse directives, clean the code and saves new code in memory
       |  3️⃣ call exec( ... ) to execute all new code
       |  4️⃣ call sys.exit(0) to stop old code execution
       |    
       3️⃣ All code after "PYPP.parse( ..." from original compiled code is DISCARDED ❌❌

Be atention to step 3.2.4. When the code is executed as a script we can stop the execution of the old code, 
because we have sure that the new code was all executed stand alone. But we still have a problem. All the code 
before ``PYPP.parse( ...`` was executed twice. Right ? Yes and No. We have tools to prevent its to happen. 
Let's see an pratical example to understand better.

So the first step is instantiate a preprocessor in our source code:

.. code:: python

    from cpypp import py_preprocessor
    PYPP = py_preprocessor()

❗️ **YOU CAN NOT** change this piece of code neither change ``PYPP.`` variable.

The reason is: When the preprocessor is doing its job, it will look for this piece of code
and some references to ``PYPP`` variable so, it can be removed from final code.

The second step is write the directives in source code to give work to the preprocessor. 
Directives are like coments and can be written anywhere in the code. All the directives and
its rules will be explained bellow.

.. code:: python

    #ifdef debug
    print("I'm a debug line running in Python __VERSION__ and won't be present in final code')
    #endif

The third step is call the preprocessor so it can do its job:

.. code:: python

    PYPP.parse(__file__, __name__)

❗️ **DON'T CHANGE** this line either.

and finally we have our ``test_script01.py`` with other little stuff as :

.. code:: python

    import sys
    from cpypp import py_preprocessor
    PYPP = py_preprocessor()

    #exclude
    if len(sys.argv) > 1 and sys.argv[1] == '-d': PYPP.define("debug")
    #endexclude

    print("PRINT me always but just once. I'm using Python __VERSION__ !!!")
    PYPP.parse(__file__, __name__)

    #ifdef debug
    print("PRINT me only if '-d' used. I'm using Python __VERSION__ !!!")
    #endif

So, let's run it using python 3.7

::

    $ python3 -m cpypp.tests.test_script01
    PRINT me always but just once. I'm using Python __VERSION__ !!!
    PRINT me always but just once. I'm using Python 3.7.6 !!!

::

    $ python3 -m cpypp.tests.test_script01 -d
    PRINT me always but just once. I'm using Python __VERSION__ !!!
    PRINT me always but just once. I'm using Python 3.7.6 !!!
    PRINT me only if '-d' used. I'm using Python 3.7.6 !!!

Well, it didn't work as expected  😩. The first print was executed twice. The reason was 
explained earlier. All code before ``PYPP.parse( ...`` is executed at original code and at 
preprocessed code. To solve this we have many options. First let's understand that this happens
only to code that starts at column 1 (usually), with exception to classes and functions declarations. 
All code inside classes and funcions are executed only when called, but all the rest is executed 
instantly.

The options to solve this issue are:

#. Move ``PYPP.parse( ...`` next to top of code so, there is no relevant code before it, but only the  
   necessary to its own execution.

#. Use the special logical condition ``if PYPP.parsed():`` to all relevant code before ``PYPP.parse( ...``. This
   will prevent this code to be executed because this condition returns always ``False``, so nothing inside will
   be executed with original code. The preprocessor recognizes this special logical condition, removes it 
   completely from final code and reident the code to it's original position.

With option 1 we have ``test_script02.py``:

.. code:: python

    import sys
    from cpypp import py_preprocessor

    #exclude
    if len(sys.argv) > 1 and sys.argv[1] == '-d': PYPP.define("debug")
    #endexclude

    PYPP.parse(__file__, __name__)

    print("PRINT me always but just once. I'm using Python __VERSION__ !!!")

    #ifdef debug
    print("PRINT me only if '-d' used. I'm using Python __VERSION__ !!!")
    #endif

With option 2 we have ``test_script03.py``:

.. code:: python

    import sys
    from cpypp import py_preprocessor
    PYPP = py_preprocessor()

    # This is just a comment

    #exclude
    if len(sys.argv) > 1 and sys.argv[1] == '-d': PYPP.define("debug")
    #endexclude

    if PYPP.parsed():
       print("PRINT me always but just once. I'm using Python __VERSION__ !!!")

       #ifdef debug
       print("PRINT me only if '-d' used. I'm using Python __VERSION__ !!!")
       #endif

    PYPP.parse(__file__, __name__)

So, let's try again ...

::

    $ python3 -m cpypp.tests.test_script02
    PRINT me always but just once. I'm using Python 3.7.6 !!!

::

    $ python3 -m cpypp.tests.test_script03 -d
    PRINT me always but just once. I'm using Python 3.7.6 !!!
    PRINT me only if '-d' used. I'm using Python 3.7.6 !!!

Yeah 😁. So the first rule of cpypp is that for scripts, we have to keep our ``PYPP.parse( ...`` call as next from top 
of code we can, or use ``if PYPP.parsed():`` logical condition, or both, so our code can be processed the way we
wants. Another very important rule is:

❗️ Your original source code **HAS TO BE** compilable in all Python versions, because this original source code has to
run so the processor can do its job.

This means that a code like:

.. code:: python

    #ifdef __PYTHON2__
    print "This is", "a debug code ", "and will NOT run  in Python 3"
    #else
    print("This is a debug code and is executes if we are using Python 3")
    #endif

will not compile in Python 3 because  second line will generate a syntax error. In these case if you can't change the original code you can use the directive ``#expand`` as you see bellow.

.. code:: python

    #ifdef __PYTHON2__
    #expand print "This is", "a debug code ", "and will NOT run  in Python 3"
    #else
    print("This is a debug code and is executes if we are using Python 3")
    #endif

How Python and cpypp works when source code is a module to be imported
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now, let's see a graphical flow how Python and cpypp will do their job to guarantee that the preprocessor will work
properly when importing a module

::

    Flow
    |
    1️⃣ Another Python scripts or module imports our original .py  file
    2️⃣ Python reads original .py module file
    3️⃣ compiles it in memory (.pyc)
    4️⃣ loads, runs the compiled code and inserts an entry for it in ``sys.modules``
       |
       1️⃣ All code before "PYPP.parse( ..." is executed ✅✅
       2️⃣ When "PYPP.parse( ..." is called
       |  |
       |  1️⃣ PYPP reads original .py file
       |  2️⃣ parse directives, clean the code and save new code in a file
       |  3️⃣ call __import__( ... ) to load the new code in the same ``sys.modules`` entry
       |  4️⃣ new code is executed
       |    
       3️⃣ All code after "PYPP.parse( ..." from original compiled code IS EXECUTED TOO ✅✅

There are diferences from a script code. We have ``sys.modules`` that has to be modified at runtime, we can't call
``sys.exit`` because Python will halt and the most important, when the source file is 
a module to be imported **all the original code will be executed** no matter which place you write 
``PYPP.parse( ...``. So we **HAVE** to use ``if PYPP.parsed():`` logical condition to prevent our code to be executed twice and avoid unpredictable runtime errors write ``PYPP.parse(...`` after all references to ``PYPP.`` in source code. Let's see some pratical examples to understand better. 

You can protect only what is relevant. See ``import4.py``

.. code:: python

    import os
    from cpypp import py_preprocessor
    PYPP = py_preprocessor()

    class test_class(): # classes and functions are not a problem because are only compiled

          def __init__(self):
              print("This print has no problem")

    GLOBAL_VARIABLE = "PYTHON vr __VERSION__" 
    # global variable definitions are most of time safe to become unprotected

    if PYPP.parsed(): # but code like this has to be protected at all

       if os.path.isfile("/tmp/test.txt"):
          os.remove("/tmp/test.txt")

       print("module import4 imported and I was printed just once")

    PYPP.parse(__file__, __name__)

Or you can protect the all code. See ``import5.py``

.. code:: python

    import os
    from cpypp import py_preprocessor
    PYPP = py_preprocessor()

    if PYPP.parsed(): # You can protect the all code

       class test_class(): # classes and functions are not a problem because are only compiled

             def __init__(self):
                 print("This print has no problem")

       GLOBAL_VARIABLE = "PYTHON vr __VERSION__" 
       # global variable definitions are most of time safe to become unprotected

       if os.path.isfile("/tmp/test.txt"):
          os.remove("/tmp/test.txt")

       print("module import5 imported and I was printed just once")

    PYPP.parse(__file__, __name__)

Or you can protect nothing if you code has only global, classes and defs definitions. See ``test06_import_module.py``

.. code:: python

    from cpypp import py_preprocessor
    PYPP = py_preprocessor()

    GLOBAL_VARIABLE = "PYTHON vr __VERSION__" 
    # global variable definitions are most of time safe to become unprotected
    class test_class(): # classes and functions are not a problem because are only compiled

          def __init__(self):
              print("This print has no problem")

    print("I don't care if this line is printed twice")

    PYPP.parse(__file__, __name__)

Let's import all of then

>>> cpypp.tests.imports import impor4
module import4 was imported and I was printed just once
>>> cpypp.tests.imports import impor5
module import5 was imported and I was printed just once
>>> cpypp.tests.imports import impor6
I don't care if this line is printed twice
I don't care if this line is printed twice

Yeah again😁. Here the rule is that for import modules, we have to use ``if PYPP.parsed():`` logical condition, in the whole code if necessary, and write ``PYPP.parse (...`` at the end of our source code, so our code can be processed the way we wants. 

Another thing that is very important:

| ❗️ ``if PYPP.parsed():`` logical condition, **CAN ALSO** be replaced by ``if False and False:``. 
| ❗️ cpypp will understand this too.

Command line preprocessor
-------------------------

Command line preprocessor is when you have source code files and wants to generate new preprocessed files in
batch mode. Probably you are a developer and want to insert copyright marks, or remove something from final code, like
``prints``, debugs and so on, or you know exactly what version of Python will execute your code and wants to
generate a final code totally compatible with it. Almost like C does with ``make``.

Here we have no flow. It's just a command line tool that has some parameters and you can run it from shell.

::

    $ python2.7+ -m cpypp -r -d debug cpypp./tests/test_commandline01.pyp 

❗️ The code generated is **DIRECTLY DEPENDENT** from the Python version you run the command line

Options
^^^^^^^

Usage: ``cpyppc [options] filename-or-directory [...]``

-h, --help        show this help message and exit
-v, --version     print cpypp version
-d name           same as #define. Ex. ``-d`` debug or ``-d "var=2+2"`` (eval 4)
-e EXT            include files with only these extensions. default is ``'.py'``
                  and extensions must be separated with ``'|'`` char. Ex.
                  ``'.py|.pypp'``
-l MAXLEVELS      levels to recurse into subdirectories. Use ``'0'`` to don't
                  recurse. Default is no limit
-p PATH           directory to prepend to file names and paths before save
                  processed files. The full path will be created if it does
                  not exists
-f                force overwrite of files when output file name has the
                  same name of input file name
-r                remove meta tags and commented lines from final code
-o FILE           output file name when you are preprocessing just one file
                  at once. Use ``'-o -'`` to stdout
-q                output only error messages; ``-qq`` will suppress the error
                  messages as well
-c, --compileall  compile each file after preprocessing. When this option is
                  used, no preprocessed source file will be saved to disk and
                  options ``'-o'``, ``'-r'`` and ``'-f'`` are discarded
-b                use legacy (pre-PEP3147) compiled file locations. Valid
                  only when ``'-c'`` is used

Examples
^^^^^^^^

Let's use one of our script files ``test_script03.py``

.. code:: python

    import sys
    from cpypp import py_preprocessor
    PYPP = py_preprocessor()

    # This is just a comment

    #exclude
    if len(sys.argv) > 1 and sys.argv[1] == '-d': PYPP.define("debug")
    #endexclude

    if PYPP.parsed():
       print("PRINT me always but just once. I'm using Python __VERSION__ !!!")

       #ifdef debug
       print("PRINT me only if '-d' used. I'm using Python __VERSION__ !!!")
       #endif

    PYPP.parse(__file__, __name__)

Now let's run ``cpypp`` and don't remove metada to see all preprocessor work.

::

    $ python3 -m cpypp cpypp./tests/test_script03.py -o -  

.. code:: python
 
    import sys
    # from cpypp import py_preprocessor
    # PYPP = py_preprocessor()

    # This is just a comment

    # #exclude
    # if len(sys.argv) > 1 and sys.argv[1] == '-d': PYPP.define("debug")
    # #endexclude

    # if PYPP.parsed():
    print("PRINT me always but just once. I'm using Python 3.7.6 !!!")

    # #ifdef debug
    # print("PRINT me only if '-d' used. I'm using Python __VERSION__ !!!")
    # #endif

Realize that any references to ``py_preprocessor`` were commented and the block ``if PYPP.parsed():`` 
has been commented too and all code bellow was reidented.
Let's remove metada data now.

::

    $ python3 -m cpypp -r cpypp/tests/test_script03.py -o -  

.. code:: python
 
    import sys

    # This is just a comment

    print("PRINT me always but just once. I'm using Python 3.7.6 !!!")


❗️ As you can see there is **NO DEPENDENCY** in final code from cpypp.

Preprocessing and compiling code at once
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

cpypp can compile bytecode files (.pyc) directly from the preprocessed file without need to save the new file to
disk an execute ``python -m compileall``, and is as simple as this. Just use ``-c`` or ``--compileall`` option.

::

    $ python -m cpypp --compileall diretory_or_file      # generate __pycache__/.pyc files
    $ python -m cpypp -b --compileall diretory_or_file   # generate .pyc files at same dir

Your bytecodes (.pyc) where generated using the preprocessed file and are ready to deploy. For more 
information and usage execute ``python cpypp --help``.

Expander
========

cpypp implements some expanders that look for names and special characters in the source code and replace then
for defined values or expressions.

Name definitions expander
-------------------------

Any references to name definitions done with ``#define`` in source file will be replaced by its ``repr()`` value.
Note than any references means any place where definition names appears, even inside strings. To avoid this
replacement precede the name with ``'!'``
For example, the code:

.. code:: Python
    
    #define SIZE 100 * 2
    #define TEXT "cpypp" + " is " + "the best"

    for i in range(0, SIZE): print(TEXT)
    print("The value of !TEXT is TEXT")

after preprocessing will become:

.. code:: Python
    
    for i in range(0, 200): print('cpypp is the best')
    print("The value of TEXT is 'cpypp is the best'")

Expressions expander
--------------------

For more complexes replacements there is expression expander. All text between expander begin mark ``'#{'`` and
expander end mark ``}#'`` will be evaluated and replaced exactly at same place by its ``str()`` value. If you wants
that replacement value be by its ``repr()`` value, insert a modifier at end of expression, without spaces from ``'}'``.
The modifiers are ``',s`` for ``str()`` value and ``',r'`` for ``repr()`` value.
For example, the code:

.. code:: Python

    #! env python#{__VERSION__[0]}#
    
    #define VALUE 5 if __PYTHON2__ else 6
    #define TEXT "cpypp" + " is " + "the best"

    print("!VALUE + 1 = #{VALUE + 1}# and #{TEXT}# and #{TEXT,r}#")

after preprocessing with ``python2`` will become:

.. code:: Python

    #! env python2
    
    print("VALUE + 1 = 6 and cpypp is the best and 'cpypp is the best'")

and after preprocessing with ``python3`` will become:

.. code:: Python

    #! env python3
    
    print("VALUE + 1 = 7 and cpypp is the best and 'cpypp is the best'")

Directives
==========

Name definitions (#define, #undef)
----------------------------------

Define names, or names with values that will be stored in definition dictionary.

``#define identifier [expression]``

When the preprocessor encounters this directive, it creates an entry in its definition dictionary with name ``identifier`` and the value with evaluation of ``expression``. If ``expression`` is ommited, ``True`` is used. 

.. code:: Python

    #define DEBUG
    #define TABLE_SIZE (50 * 50 if __PYTHON2__ else 100 * 100)

    block = list(" " * TABLE_SIZE)

    #ifdef DEBUG
    print("Debug is ON !!!")
    #endif

To remove an entry from definition dictionary use 

``#undef identifier``

Conditional inclusions (#if, #else, #endif and its variations)
-----------------------------------------------------------------

These directives allow to include or discard part of the original code, also called code blocks if a certain 
condition is met or not.
It works the same manner that ``if/elif/else`` in python. The diference is that we have ``#endif`` and its
variations to close opened ``#if blocks`` cause we don't have identation and there are more directives 
that gives more flexibility.

Here are all the conditional inclusions directives and how they are evalueted.

+---------------------------------+-----------------------------------------------------------------------------------+
| **#ifdef** ``identifier``       | | Opens a block of code and includes its content if ``identifier`` is a name      |
|                                 | | in definition dictionary, no matter its value.                                  |
+---------------------------------+-----------------------------------------------------------------------------------+
| **#ifndef** ``identifier``      | | Open a block of code and includes its content if ``identifier`` is not a name   |
|                                 | | in definition dictionary.                                                       |
+---------------------------------+-----------------------------------------------------------------------------------+
| **#if** ``expression``          | | Open a block of code and includes it if ``expression`` is evaluated to ``True``.|
+---------------------------------+-----------------------------------------------------------------------------------+
| **#else**                       | | Closes the last opened block of code,  opens a new block of code                |
|                                 | | and includes it if any block above and at same level was not ``True``           |
+---------------------------------+-----------------------------------------------------------------------------------+
| **#elif** ``expression``        | | Closes the last opened block of code,  opens a new block of code                |
|                                 | | and includes it if  ``expression`` is evaluated to ``True`` and any block       |
|                                 | | above and at same level was not ``True``                                        |
+---------------------------------+-----------------------------------------------------------------------------------+
|**#elifdef** ``identifier``      | | Closes the last opened block of code,  opens a new block of code                |
|                                 | | and includes it if ``identifier`` is a name in definition dictionary,           |
|                                 | | no matter its value and any block above and at same level was not ``True``.     |
+---------------------------------+-----------------------------------------------------------------------------------+
| **#endif**                      | | Closes the last opened block of code at same level                              |
+---------------------------------+-----------------------------------------------------------------------------------+
| **#endififdef** ``identifier``  | | Same as **#endif** + **#ifdef** but at the same line                            |
+---------------------------------+-----------------------------------------------------------------------------------+
| **#endifif** ``expression``     | | Same as **#endif** + **#if** but at the same line                               |
+---------------------------------+-----------------------------------------------------------------------------------+
| **#endifall**                   | | Close all opened blocks no matter if they are inner or outter. Use with care.   |
+---------------------------------+-----------------------------------------------------------------------------------+

Examples of Conditional inclusions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: Python

    # compile block if DEBUG was defined before

    #ifdef DEBUG
    print("Debug is ON !!!")
    #endif

    # compile block if DEBUG was not defined or was excluded from definition dictionary 

    #undef DEBUG
    #ifndef DEBUG
    print("Debug is ON !!!")
    #endif

    # compile block if expression is True

    # define INT_VER int(VERSION[0])
    #if DEBUG is True and INT_VER > 2
    print("Debug is ON and Python is 3+!!!")
    #elif INT_VER == 2
    print("Python certainly is 2.x")
    #else
    print("I'm sure Debug is ON or OFF :)")
    #endif

Exclusion blocks (#exclude and #endexclude)
-----------------------------------------------------------------

Depending of your code, sometimes you want to exclude an entire block of code if some conditions are met or not
or not, or  maybe you wants that only the preprocessor executes this portion of code, but wants remove this 
portion from final code. For this we have the directives **#exclude** and **#endexclude**. All inside this two directives will be completely exclude from final code, but will be seen by preprocessor.

.. code:: Python

   #exclude
   import numpy
   #endexclude

   #define NUMPY_E numpy.e
   #define NUMPY_EULER_GAMA numpy.euler_gama
   numpy_e = NUMPY_E
   numpy_euler_gama = NUMPY_EULER_GAMA

We imported numpy package only at preprocessor time to get the values of these two constants and set two local
variables. ``numpy`` package won't be needed at the machine where the final code will execute. Neither cpypp as 
we already know.

Ignore blocks (#ignore and #endignore)
-----------------------------------------------------------------

These directives do exactly what their name says. They ignore from the preprocessor an entire block of code.

.. code:: Python

   #ignore
   #define NONE "This defines will never occurs because this block is ignored"
   #ifndef NONE
   print("This !TEXT will be printed exactly how it is #{PRINT_ME#}") # Will print always
   #endif
   #endignore

Source file inclusion (#include and #includeident)
-----------------------------------------------------------------

When the preprocessor finds an ``#include`` or ``#includeident`` directive it replaces it by the entire 
content of the specified file. The diference between ``#include`` and ``#includeident`` is that 
``#include`` will always include each line of included file starting of column 1 and ``#includeident`` will
always include each line of incuded file starting at same column where ``#includeident`` was written. 
There are two ways to use #include:

+-----------------------------+------------------------------------------------------------------------------------+
| **#include** ``<filename>`` | | When filename is specified between angle-backets, cpypp looks for the            |
|                             | | filename in all directories listed in ``sys.path``. The first existing file      |
|                             | | will be included.                                                                |
+-----------------------------+------------------------------------------------------------------------------------+
| **#include** ``expression`` | | When filename is not specified between angle-brackes, cpypp assumes that this    |
|                             | | is an expression, evaluates it and the result as used as  absolute path of file. |
|                             | | If the file exists it will be included.                                          |
+-----------------------------+------------------------------------------------------------------------------------+

Supose that ``include.py`` has the following content.

::

    print("I'm an included file")

Now let's see this code.

.. code:: Python

   #include "include.py"
       #include "include.py"

   if some_condition:
      #includeident "include.py"

If we check the preprocessed file we will find:

.. code:: Python

   print("I'm an included file")
   print("I'm an included file")

   if some_condition:
      print("I'm an included file")

Code protection (#expand)
-------------------------

As you remember, the original code is compiled twice, one before the preprocessor and other after.
So at both compiling steps the code must be correct and without syntax or grammar errors.

Sometimes we want to implement some features in our code that are not available in all Python versions,
but we need that our code compile correctly so the preprocessor can do its work. For this we have ``#expand``
directive. If you had a piece of code that is not compatible with all versions of Python you put it as parameter 
of ``#expand``. The first step of compiling will consider this line as a comment and will ignore it. And the 
preprocessor will do its job. For example:

.. code:: Python

  #if __PYTHON2__
  print "This","is", "a","python","program"
  #else
  print ("This is a python program")
  #endif

The code above will generate a compile error if we try to run it on Python 3+, because the first ``print`` statement
does not meet the Python 3 syntax. So the solution is to hide this code from first compiling. ``#expand`` will do
this for us.

.. code:: Python

  #if __PYTHON2__
  #expand print "This","is", "a","python","program"
  #else
  print ("This is a python program")
  #endif

Now the first compiling will occur with no problem no matter what Python version is used 
and the preprocessor will go on.


Contributing
============

Please send an email to `wellrats@gmail.com <mailto:wellrats@gmail.com>`_
