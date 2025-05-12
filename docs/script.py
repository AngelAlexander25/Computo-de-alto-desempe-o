from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt

# Conectar con Elasticsearch especificando el esquema (http o https)
es = Elasticsearch([{'scheme': 'http', 'host': 'localhost', 'port': 9201}])

# Definir el query para obtener los datos (puedes ajustar el índice según el nombre de tu índice)
query = {
    "query": {
        "match_all": {}
    }
}

# Buscar los datos en Elasticsearch
response = es.search(index="lionel_messi_data", body=query)  # Asegúrate de que el índice sea el correcto

# Extraer los datos del 'hits' de la respuesta
data = [hit['_source'] for hit in response['hits']['hits']]

# Convertir los datos en un DataFrame
df = pd.DataFrame(data)

# Asegúrate de que las columnas estén correctamente nombradas y procesar las fechas
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convertir la columna 'Date' a datetime
df['Season'] = df['Date'].dt.year  # Extraer el año de la fecha para la temporada

# Contar los goles por temporada
season_counts = df['Season'].value_counts().sort_index()

# Graficar los goles por temporada
plt.figure(figsize=(10, 6))
season_counts.plot(kind='bar', color='crimson')
plt.title('Goles de Lionel Messi por Temporada (Barcelona)')
plt.xlabel('Temporada')
plt.ylabel('Número de Goles')
plt.xticks(rotation=45)
plt.tight_layout()

# Guardar la imagen como un archivo PNG
plt.savefig('messi_goals_by_season.png')

# Mostrar la gráfica
plt.show()
