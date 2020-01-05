import sys
sys.path.insert(1,".")
from cpypp import py_preprocessor
PYPP = py_preprocessor()

if PYPP.parsed():
   print("This print is AFTER module 'import3' is preprocessed. Using vr #{__VERSION__}#")

PYPP.parse(__file__, __name__)
