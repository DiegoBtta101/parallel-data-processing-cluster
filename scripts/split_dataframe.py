# split_dataframe.py

import pandas as pd
import numpy as np

# Cargar el DataFrame completo desde el volumen compartido
df = pd.read_csv('/data/Datos_Hidrometeorologicos.csv')

# Dividir el DataFrame en 3 partes y guardar cada una en el volumen compartido.
df_split = np.array_split(df, 3)
for i, part in enumerate(df_split):
    part.to_csv(f'/data/df_part_{i}.csv', index=False)

# End