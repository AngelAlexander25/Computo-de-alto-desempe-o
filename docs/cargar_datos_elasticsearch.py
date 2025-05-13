from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import pandas as pd
import uuid
import json

# Script para cargar datos de Messi desde CSV a Elasticsearch

# Conexión a Elasticsearch
es = Elasticsearch(
    cloud_id="https://my-elasticsearch-project-c267e7.es.us-east-1.aws.elastic.cloud:443",
    basic_auth=("elastic", "eVNZcHg1WUJIbEJDY3RlR3VtSzg6U2ttTzRCbk40TFV4eHZsbDFGRnkxUQ==")
)

# Verificar la conexión
if not es.ping():
    print("Error de conexión a Elasticsearch")
    exit(1)

print("Conexión exitosa a Elasticsearch")

# Cargar el archivo CSV
try:
    df = pd.read_csv('messi_barca.csv', encoding='cp1252')
    print(f"CSV cargado correctamente. Se encontraron {len(df)} filas.")
except Exception as e:
    print(f"Error al cargar el CSV: {e}")
    exit(1)

# Verificar las columnas del CSV
print("\nColumnas encontradas en el CSV:")
print(df.columns.tolist())

# Limpiar y convertir los datos
try:
    # Convertir columnas numéricas
    numeric_columns = ['Age', 'Matches Played', 'Starts', 'Minutes played', 
                     'Goals scored', 'Assists', 'PK', 'PKatt', 'CrdY', 'CrdR']
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convertir columnas de tasas a float
    float_columns = ['Goal/90', 'Ast/90', 'G+A/90', 'G-PK/90', 'G+A-PK/90']
    for col in float_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).replace({',': '.'}, regex=True).astype(float)
    
    # Convertir columnas de texto a string
    df['Season'] = df['Season'].astype(str)
    df['Competition'] = df['Competition'].astype(str)
    
    # Rellenar valores NaN
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    for col in float_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0.0)
    
    df['Competition'] = df['Competition'].fillna('No Competition')
    
    print("\nDatos limpios y convertidos correctamente")
    
except Exception as e:
    print(f"Error al limpiar los datos: {e}")
    exit(1)

# Definir el nombre del índice
index_name = "messi_stats"

# Verificar si el índice ya existe y eliminarlo si es necesario
if es.indices.exists(index=index_name):
    print(f"El índice {index_name} ya existe. Eliminándolo...")
    es.indices.delete(index=index_name)

# Crear el índice con mapeo explícito
print(f"Creando índice {index_name}...")
mappings = {
    "mappings": {
        "properties": {
            "Season": {"type": "keyword"},
            "Age": {"type": "integer"},
            "Competition": {"type": "keyword"},
            "Matches Played": {"type": "integer"},
            "Starts": {"type": "integer"},
            "Minutes played": {"type": "integer"},
            "Goals scored": {"type": "integer"},
            "Assists": {"type": "integer"},
            "PK": {"type": "integer"},
            "PKatt": {"type": "integer"},
            "CrdY": {"type": "integer"},
            "CrdR": {"type": "integer"},
            "Goal/90": {"type": "float"},
            "Ast/90": {"type": "float"},
            "G+A/90": {"type": "float"},
            "G-PK/90": {"type": "float"},
            "G+A-PK/90": {"type": "float"}
        }
    }
}

es.indices.create(index=index_name, body=mappings)

# Preparar los datos para indexación
def generate_actions():
    for i, row in df.iterrows():
        document = row.to_dict()
        # Limpiar cualquier valor NaN o no serializable
        document = json.loads(json.dumps(document, default=str))
        yield {
            "_op_type": "index",
            "_index": index_name,
            "_id": str(uuid.uuid4()),  # Generar ID único
            "_source": document
        }

# Indexar los datos
print(f"Indexando {len(df)} documentos en Elasticsearch...")
success, failed = 0, 0

try:
    for ok, action in streaming_bulk(es, generate_actions(), max_retries=3):
        if ok:
            success += 1
        else:
            failed += 1
        
        # Mostrar progreso
        if (success + failed) % 10 == 0:
            print(f"Progreso: {success + failed}/{len(df)} documentos")
except Exception as e:
    print(f"Error durante la indexación: {e}")

print(f"\nIndexación completada: {success} documentos exitosos, {failed} fallidos")

# Verificar que los datos se hayan indexado correctamente
count = es.count(index=index_name)
print(f"Número de documentos en el índice {index_name}: {count['count']}")

# Realizar una consulta simple para verificar
query = {"match_all": {}}
results = es.search(index=index_name, query=query, size=5)
print("\nPrimeros 5 documentos en el índice:")
for i, hit in enumerate(results["hits"]["hits"], 1):
    print(f"\nDocumento {i}:")
    source = hit["_source"]
    print(f"Temporada: {source.get('Season')}")
    print(f"Competición: {source.get('Competition')}")
    print(f"Goles: {source.get('Goals scored')}")
    print(f"Asistencias: {source.get('Assists')}")

print("\nProceso completado. Los datos están listos en Elasticsearch.")