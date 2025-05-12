import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar el dataset
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "abhijithchandradas/lionel-messi-at-f-c-barcelona",
    "lionel_messi_all_goals.csv",
)

# Procesar los datos
df['Season'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
season_counts = df['Season'].value_counts().sort_index()

# Crear gráfico
plt.figure(figsize=(10, 5))
season_counts.plot(kind='bar', color='crimson')
plt.title('Goles de Lionel Messi por Temporada (Barcelona)')
plt.xlabel('Temporada')
plt.ylabel('Número de Goles')
plt.tight_layout()

# Guardar en la carpeta docs
os.makedirs("docs", exist_ok=True)
plt.savefig("docs/goals_by_season.png")

# Crear HTML simple
with open("docs/index.html", "w") as f:
    f.write("""
    <html>
      <head>
        <title>Gráfico de Goles de Messi</title>
      </head>
      <body>
        <h1>Goles de Lionel Messi por Temporada (F.C. Barcelona)</h1>
        <img src="goals_by_season.png" alt="Gráfico de goles">
      </body>
    </html>
    """)
