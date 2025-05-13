import pandas as pd
import os

print("Directorio actual:", os.getcwd())

# Leer el archivo CSV
df = pd.read_csv("C:/Users/drago/Computo-de-alto-desempe-o/doc/data/messi_barca.csv", encoding="latin1")
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('+', 'plus').str.replace('/', '_')
df = df.sort_values(by="season")

# Crear el directorio si no existe
output_dir = "docs/data"
os.makedirs(output_dir, exist_ok=True)

# Guardar el archivo JSON
df.to_json(f"{output_dir}/messi_barcelona_clean.json", orient="records", lines=True)
