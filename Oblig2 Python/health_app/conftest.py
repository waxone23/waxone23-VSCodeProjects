import sys
import os

# Add the src directory to the path so tests can find health_app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
