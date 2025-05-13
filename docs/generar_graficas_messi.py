from elasticsearch import Elasticsearch
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Configuración de la conexión a Elasticsearch
es = Elasticsearch(
    cloud_id="https://my-elasticsearch-project-c267e7.es.us-east-1.aws.elastic.cloud:443",
    basic_auth=("elastic", "eVNZcHg1WUJIbEJDY3RlR3VtSzg6U2ttTzRCbk40TFV4eHZsbDFGRnkxUQ==")
)

# Verificar la conexión
if not es.ping():
    print("Error de conexión a Elasticsearch")
    exit(1)

print("Conexión exitosa a Elasticsearch")

# Nombre del índice en Elasticsearch
index_name = "messi_stats"

# Función para obtener todos los datos de Elasticsearch
def get_messi_data():
    # Consulta para obtener todos los documentos (hasta 100)
    query = {"match_all": {}}
    results = es.search(index=index_name, query=query, size=100)
    
    # Convertir los resultados a un DataFrame
    data = [hit["_source"] for hit in results["hits"]["hits"]]
    df = pd.DataFrame(data)
    
    return df

# Crear directorio para guardar las gráficas
output_dir = "graficas_messi"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Obtener datos de Elasticsearch
df = get_messi_data()
print(f"Se obtuvieron {len(df)} registros de Elasticsearch")

# Configurar el estilo de las gráficas
plt.style.use('ggplot')
sns.set_palette("deep")

# 1. Goles por temporada
print("Generando gráfica: Goles por temporada")
season_data = df.groupby("Season")["Goals scored"].sum().reset_index()
season_data = season_data.sort_values("Season")

plt.figure(figsize=(12, 6))
plt.bar(season_data["Season"], season_data["Goals scored"], color='#004D98')
plt.plot(season_data["Season"], season_data["Goals scored"], 'o-', color='#A50044', linewidth=2)
plt.title('Goles de Messi por temporada', fontsize=16)
plt.xticks(rotation=45)
plt.xlabel('Temporada')
plt.ylabel('Goles')
plt.tight_layout()
plt.savefig(f"{output_dir}/goles_por_temporada.png")
plt.close()

# 2. Goles por competición
print("Generando gráfica: Goles por competición")
competition_data = df.groupby("Competition")["Goals scored"].sum().reset_index()
competition_data = competition_data.sort_values("Goals scored", ascending=False)

plt.figure(figsize=(12, 6))
plt.bar(competition_data["Competition"], competition_data["Goals scored"], color='#A50044')
plt.title('Goles de Messi por competición', fontsize=16)
plt.xticks(rotation=45)
plt.xlabel('Competición')
plt.ylabel('Goles')
plt.tight_layout()
plt.savefig(f"{output_dir}/goles_por_competicion.png")
plt.close()

# 3. Relación entre goles y asistencias
print("Generando gráfica: Relación entre goles y asistencias")
plt.figure(figsize=(10, 8))
sns.scatterplot(data=df, x="Goals scored", y="Assists", hue="Competition", s=100)
plt.title('Relación entre goles y asistencias por competición', fontsize=16)
plt.xlabel('Goles')
plt.ylabel('Asistencias')
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/goles_vs_asistencias.png")
plt.close()

# 4. Evolución de goles y asistencias
print("Generando gráfica: Evolución de goles y asistencias")
evolution_data = df.groupby("Season").agg({
    "Goals scored": "sum",
    "Assists": "sum"
}).reset_index()
evolution_data = evolution_data.sort_values("Season")

plt.figure(figsize=(12, 6))
plt.plot(evolution_data["Season"], evolution_data["Goals scored"], 'o-', label='Goles', linewidth=2)
plt.plot(evolution_data["Season"], evolution_data["Assists"], 's-', label='Asistencias', linewidth=2)
plt.title('Evolución de goles y asistencias por temporada', fontsize=16)
plt.xticks(rotation=45)
plt.xlabel('Temporada')
plt.ylabel('Cantidad')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/evolucion_goles_asistencias.png")
plt.close()

# 5. Distribución de goles por edad
print("Generando gráfica: Distribución de goles por edad")
age_data = df.groupby("Age")["Goals scored"].sum().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(age_data["Age"], age_data["Goals scored"], color='#004D98')
plt.title('Goles de Messi por edad', fontsize=16)
plt.xlabel('Edad')
plt.ylabel('Goles')
plt.grid(True, axis='y')
plt.tight_layout()
plt.savefig(f"{output_dir}/goles_por_edad.png")
plt.close()

# Generar un HTML simple para mostrar las gráficas
print("Generando página HTML con las gráficas")
html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estadísticas de Messi - FC Barcelona</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        header {
            background: linear-gradient(135deg, #004d98 0%, #a50044 100%);
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        h1 {
            margin: 0;
            font-size: 2em;
        }
        .chart-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 30px;
        }
        .chart-title {
            color: #004d98;
            margin-top: 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        .chart {
            text-align: center;
            margin-top: 10px;
        }
        .chart img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }
    </style>
</head>
<body>
    <header>
        <h1>Estadísticas de Lionel Messi en FC Barcelona</h1>
        <p>Visualización de datos desde Elasticsearch</p>
    </header>

    <div class="chart-container">
        <h2 class="chart-title">Goles por temporada</h2>
        <div class="chart">
            <img src="graficas_messi/goles_por_temporada.png" alt="Goles por temporada">
        </div>
    </div>

    <div class="chart-container">
        <h2 class="chart-title">Goles por competición</h2>
        <div class="chart">
            <img src="graficas_messi/goles_por_competicion.png" alt="Goles por competición">
        </div>
    </div>

    <div class="chart-container">
        <h2 class="chart-title">Relación entre goles y asistencias</h2>
        <div class="chart">
            <img src="graficas_messi/goles_vs_asistencias.png" alt="Goles vs Asistencias">
        </div>
    </div>

    <div class="chart-container">
        <h2 class="chart-title">Evolución de goles y asistencias</h2>
        <div class="chart">
            <img src="graficas_messi/evolucion_goles_asistencias.png" alt="Evolución de goles y asistencias">
        </div>
    </div>

    <div class="chart-container">
        <h2 class="chart-title">Goles por edad</h2>
        <div class="chart">
            <img src="graficas_messi/goles_por_edad.png" alt="Goles por edad">
        </div>
    </div>

    <footer>
        <p>Datos de Messi en Barcelona · Visualizaciones generadas con matplotlib y seaborn</p>
    </footer>
</body>
</html>
"""

with open(f"{output_dir}/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Proceso completado. Las gráficas se encuentran en el directorio: {output_dir}")
print(f"Abre el archivo {output_dir}/index.html para ver todas las gráficas juntas")