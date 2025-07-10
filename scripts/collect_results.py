import pandas as pd
import ast  # Para convertir el string de percentiles a un diccionario

# Leer los archivos de resultados de cada partición
results = []
for i in range(3):
    df = pd.read_csv(f'/mnt/shared/result_part_{i}.csv')
    results.append(df)

# Concatenar los DataFrames para facilidad de acceso
combined_df = pd.concat(results, ignore_index=True)

# Calcular el resultado combinado
combined_result = {
    "temperatura_promedio": combined_df["temperatura_promedio"].mean(),
    "max_value": combined_df["max_value"].max(),
    "min_value": combined_df["min_value"].min(),
    "moda": combined_df["moda"].mode().iloc[0] if not combined_df["moda"].mode().empty else None,
    "varianza": combined_df["varianza"].mean(),
    "desviacion_estandar": combined_df["desviacion_estandar"].mean(),
    "curtosis": combined_df["curtosis"].mean(),
    "asimetria": combined_df["asimetria"].mean(),
    "suma_varianza_movil": combined_df["suma_varianza_movil"].sum()
}

# Promediar los percentiles
percentiles = ["{10: 0, 25: 0, 50: 0, 75: 0, 90: 0}"] * 3  # inicializa en caso de que esté vacío
if "percentiles" in combined_df.columns:
    percentiles_list = [ast.literal_eval(p) for p in combined_df["percentiles"]]
    percentiles_avg = {k: sum(p[k] for p in percentiles_list) / len(percentiles_list) for k in percentiles_list[0]}
    combined_result["percentiles"] = percentiles_avg

# Guardar el resultado combinado en un archivo CSV
combined_result_df = pd.DataFrame([combined_result])
combined_result_df.to_csv('/mnt/shared/combined_results.csv', index=False)

print("Resultado combinado guardado en combined_results.csv")