import pandas as pd
import numpy as np
import os
from collections import Counter
import scipy.stats as stats

# Leer el número de partición del entorno
partition = os.getenv('PARTITION', '0')  # Defecto en 0 si no se establece

# Cargar la partición correspondiente del DataFrame
df = pd.read_csv(f'/mnt/shared/df_part_{partition}.csv')

# Variables para almacenar resultados
total_sum = 0
count = 0
max_value = float('-inf')
min_value = float('inf')
values_list = []
sum_squared_diff = 0
rolling_var_sum = 0
percentiles = [10, 25, 50, 75, 90]

# 1. Promedio y varianza
for valor in df['ValorObservado']:
    total_sum += valor
    count += 1
temperatura_promedio = total_sum / count

# 2. Cálculo del máximo y mínimo
for valor in df['ValorObservado']:
    if valor > max_value:
        max_value = valor
    if valor < min_value:
        min_value = valor

# 3. Moda
for valor in df['ValorObservado']:
    values_list.append(valor)
frecuencia = Counter(values_list)
moda = frecuencia.most_common(1)[0][0]

# 4. Cálculo de varianza
for valor in df['ValorObservado']:
    sum_squared_diff += (valor - temperatura_promedio) ** 2
varianza = sum_squared_diff / count

# 5. Desviación estándar
desviacion_estandar = np.sqrt(varianza)

# 6. Calcular percentiles
sorted_values = sorted(values_list)
percentile_values = {}
for p in percentiles:
    percentile_values[p] = np.percentile(sorted_values, p)

# 7. Calcular curtosis y asimetría
curtosis = stats.kurtosis(values_list)
asimetria = stats.skew(values_list)

# 8. Ventana móvil para varianza móvil (ventana de 500 elementos)
window_size = 500
for i in range(window_size, len(values_list)):
    window = values_list[i-window_size:i]  # Subconjunto de la ventana
    rolling_var_sum += np.var(window)

# Guardar resultados en un archivo CSV específico para esta partición
results = {
    "temperatura_promedio": temperatura_promedio,
    "max_value": max_value,
    "min_value": min_value,
    "moda": moda,
    "varianza": varianza,
    "desviacion_estandar": desviacion_estandar,
    "percentiles": percentile_values,
    "curtosis": curtosis,
    "asimetria": asimetria,
    "suma_varianza_movil": rolling_var_sum
}

# Convertir a DataFrame para guardar
results_df = pd.DataFrame([results])
results_df.to_csv(f'/mnt/shared/result_part_{partition}.csv', index=False)

