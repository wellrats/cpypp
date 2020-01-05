import sys
from cpypp import py_preprocessor
PYPP = py_preprocessor()

#exclude
if len(sys.argv) > 1 and sys.argv[1] == '-d': PYPP.define("debug")
#endexclude

PYPP.parse(__file__, __name__)

print("PRINT me always but just once. I'm using Python #{__VERSION__}# !!!")

#ifdef debug
print("PRINT me only if '-d' used. I'm using Python #{__VERSION__}# !!!")
#endif
