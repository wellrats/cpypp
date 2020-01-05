from cpypp import py_preprocessor
PYPP = py_preprocessor()

GLOBAL_VARIABLE = "PYTHON vr __VERSION__"
# global variable definitions are most of time safe to become unprotected
class test_class(): # classes and functions are not a problem because are only compiled

      def __init__(self):
          print("This print has no problem")

print("I don't care if this line is printed twice")
PYPP.parse(__file__, __name__)
