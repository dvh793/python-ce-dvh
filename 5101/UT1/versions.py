import matplotlib
import numpy as np
import pandas as pd
import sklearn

print("NumPy", np.__version__)
print("pandas", pd.__version__)
print("Matplotlib", matplotlib.__version__)
print("scikit-learn", sklearn.__version__)

import numpy as np

a = np.array([3.5, 2.1, 0.0, 4.8])      # desde una lista
b = np.arange(0, 24)                     # 0, 1, ..., 23
c = np.zeros((3, 4))                     # matriz 3x4 de ceros
d = np.linspace(0, 1, 5)                 # 5 valores entre 0 y 1

print(a.dtype, a.shape, a.ndim)
print(b.reshape(4, 6).shape)
print(d)
