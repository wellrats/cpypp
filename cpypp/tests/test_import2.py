import sys
sys.path.insert(1, ".")

"""
test_import2.py"

This test will import a module who imports another module who
imports another module and all three al preprocessed. 
Works like a charm !!!
"""

dashes = "-" * 30

print("\n" + dashes + " begin of import " + dashes + "\n") 
from imports import import1
print("\n" + dashes + "  end of import  " + dashes + "\n") 

print([k for k in sys.modules.keys() if "imports" in k])
