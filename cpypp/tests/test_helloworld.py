from cpypp import py_preprocessor
PYPP = py_preprocessor()
PYPP.parse(__file__, __name__)

print("Hello world from Pytpp running in Python #{__VERSION__}#")

