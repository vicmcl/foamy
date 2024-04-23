import sys
sys.path.append(__file__.split("tests")[0])

import numpy as np
import pandas as pd

from utils.impute import Filler

data = {
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, 7, 8],
    'C': [np.nan, np.nan, np.nan, np.nan]  # Entire column filled with NaN
}

df = pd.DataFrame(data)

fl = Filler()
df_imputed = fl.fit_transform(df)
print(df_imputed)

