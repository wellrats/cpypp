import os
import sys
sys.path.insert(1, os.path.dirname(__file__))

print("\n" + "-" * 30 + " begin of import " + "-" * 30 + "\n") 

import imports
from imports.functions import *

print("\n" + "-" * 30 + "  end of import  " + "-" * 30 + "\n") 

print([k for k in sys.modules.keys() if "imports" in k])
print(imports.functions.pyt_ver1, pyt_ver2)
print(user_test())
print(class_test().__class__.__name__)
