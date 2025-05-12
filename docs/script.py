import kagglehub
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Descargar el dataset
dataset_path = kagglehub.dataset_download("abhijithchandradas/lionel-messi-at-f-c-barcelona")

# 2. Cargar el CSV
csv_path = os.path.join(dataset_path, "lionel_messi_all_goals.csv")
df = pd.read_csv(csv_path)

# 3. Procesar: contar goles por temporada
df['Season'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
season_counts = df['Season'].value_counts().sort_index()

# 4. Crear gráfico
plt.figure(figsize=(10, 5))
season_counts.plot(kind='bar', color='crimson')
plt.title('Goles de Lionel Messi por Temporada (Barcelona)')
plt.xlabel('Temporada')
plt.ylabel('Número de Goles')
plt.tight_layout()

# 5. Guardar gráfico en docs/
os.makedirs("docs", exist_ok=True)
plt.savefig("docs/goals_by_season.png")


