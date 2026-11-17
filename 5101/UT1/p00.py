# p00.py
import sys
from pathlib import Path

import numpy
import openpyxl
import pandas
import pyarrow
import sqlalchemy

print(sys.executable)                       # debe terminar en .venv/.../python
print("numpy", numpy.__version__, "| pandas", pandas.__version__)
print("sqlalchemy", sqlalchemy.__version__, "| pyarrow", pyarrow.__version__)

for ruta in ["datos/bd/northwind.db", "datos/bd/chinook.db",
             "datos/alisios/limpio/instalaciones.csv", "datos/alisios/sucio/clientes.csv"]:
    print(Path(ruta).exists(), ruta)        # True si el fichero esta donde debe
