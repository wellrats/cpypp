# module1.py

'''
module1.py - Python2x and Python3x module to be imported that
can run different code for different python interpreters.
'''

import sys
sys.path.insert(1, ".")

from cpypp import py_preprocessor
PYPP = py_preprocessor()

## all inside exclude blocks will not go to final code 
## PYPP.define only works in "run mode". Do not use it on
## batch mode. Use: -d option, see: python -m cpypp -h

#exclude

if sys.version[:3].split('.')[0] == '2': PYPP.define('python2')
if sys.version[:3].split('.')[0] == '3': PYPP.define('python3')
#endexclude

# This module will be imported once, than rewriten, recompiled and
# imported again, so we must avoid at most in first importing do 
# stuff that are not inside functions or classes. One elegant way
# to do this is use 'if PYPP.parse( ...'. All inside the if only
# will be executed at second time, because 'parse' always returns
# false

print("Only this message will be printed twice ...")

if PYPP.parsed():

    print("... see tests/imports/functions.py to know why")
    class class_test(): pass

    def user_test(): return "inside user_test()";

    # expander example

    print('Hi. This code was generated using Python vr. #{__VERSION__}#')

    ## ifdef .. elifdef example
    ## ------------------------

    #ifdef __PYTHON2__
    print('Generated using Python 2x (tested with internal !__PYTHON2__)')
    #elifdef __PYTHON3__
    print('Generated using Python 3x (tested with internal !__PYTHON3__)')
    #else
    print('Python version not supported')
    #endif

    ## ifdef .. endifall example
    ## runtime user defined names
    ## --------------------------

    #\/\/ will be closed by #ifdefall bellow
    #ifdef __BATCH_MODE__

    print("warning: #define at runtime using PPY.define only works in run mode.")
    print("         this code was generated in batch mode.")

    #else

    # nested ifs example

    #ifdef python2 
    print('Generated using Python 2x (tested with runtime user defined !python2)')
    #else

    #ifdef python3
    print('Generated using Python 3x (tested with runtime user defined !python3)')
    #else
    print('python2 and python3 do not exists in "batch mode"')
    #endif

    #endif

    ## undef example
    ## -------------

    #undef python2
    #undef python3

    # \/\/ will be closed by #ifdefall bellow
    #ifdef python2 
    print('Generated using Python 2x (tested with user defined !python2)')
    #else
    #ifdef python3
    print('Generated using Python 3x (tested with user defined !python3)')
    #else
    print("user defined 'python2' and 'python3' do not exists anymore")

    #endifall
    ## /\/\/\ closes this #ifdef block and #ifdef __BATCH_MODE__ above

    ## example of define expressions
    ## -----------------------------

    #define COUNT1 (1+1) * 2
    #if COUNT1 > 5
    print("#define !COUNT1 is greater than 5")
    #else
    print("#define !COUNT1 is less than 5")
    #endif

    ## example of complex define expressions 
    ## -------------------------------------

    #define COUNT2 COUNT1 + (2 if __VERSION__ > "3" else 1)
    #if COUNT2 == 6
    print("#define !COUNT2 is #{COUNT2}# because this source was generated using Python #{__VERSION__[0]}#x")
    #else
    print("#define !COUNT2 is #{COUNT2}# because this source was generated using Python 2x")
    #endif

    ## this code bellow will only work in batch mode
    ## so, if you uncomment it use command line to generate .py file
    ## otherwise you will throw an compiler exception

    if True:

        # when using run mode, the all code is loaded and compiled twice. 
        # The first one is at the time you call the program from command line and
        # the other the time you call PPY.parse().

        #ignore
        # Expanded expressions which are inside #{ and }# will be loaded and compiled once and
        # expanded only after PPY.parse call.
        #endignore

        # So, if you use expansion delimiters that does not meets Python syntax it will 
        # generates  an error at the program load. To avoid this you can use '#expand' directive
        # which force a line to be expanded and compiled only after to PPY.parse()

        # The line bellow is syntatically perfect so it will compile on both stages and be
        # expanded at second stage

        pyt_ver1 = "#{__VERSION__}#"; mode1="#{__MODE__}#";

        # The line bellow do not meets the Python syntax so it can not be compiled at
        # first stage, so we have to hide it with #expand directive

        # Note that identation is preserved when you use #expand directive

        #expand pyt_ver2 = #{__VERSION__,r}#; mode2=#{__MODE__,r}#; 

        pass

    line = "This code was generated using Python vr. {}, using {} mode"
    print(line.format(pyt_ver1, mode1))
    #expand print(line.format(pyt_ver2, mode2))
    user_test()

PYPP.parse(__file__, __name__)

