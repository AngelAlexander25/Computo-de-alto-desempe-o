import pandas as pd
from elasticsearch import Elasticsearch

# Leer CSV
df = pd.read_csv("messi_barca.csv")

# Conexión a Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Nombre del índice
index_name = "messi_barcelona_stats"

# Eliminar si ya existe
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Insertar fila por fila
for _, row in df.iterrows():
    es.index(index=index_name, document=row.to_dict())

print("Datos cargados en Elasticsearch.")
