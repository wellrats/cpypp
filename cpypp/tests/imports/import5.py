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
