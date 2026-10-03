# put src/ on the import path so tests can import gpa_calculator and app without installing them
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
