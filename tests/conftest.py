import os
import sys
import pathlib

# Asegurar que la raíz del proyecto esté en sys.path para importar 'src'
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
