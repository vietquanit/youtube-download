import sys
import os
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")
try:
    import flask
    print(f"Flask version: {flask.__version__}")
except ImportError as e:
    print(f"ERROR: {e}")
