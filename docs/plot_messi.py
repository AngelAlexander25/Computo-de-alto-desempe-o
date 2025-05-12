import pandas as pd
import plotly.express as px

# Leer el dataset real
df = pd.read_csv("messi-barca.csv")
df['Season'] = df['Season'].astype(str)
df['Goals'] = pd.to_numeric(df['Goals'], errors='coerce')

# Crear gráfico con etiquetas en español
fig = px.bar(df, x='Season', y='Goals', title='Goles de Messi por temporada en el Barcelona',
             labels={'Season': 'Temporada', 'Goals': 'Goles'})

# Guardar imagen (NO generar HTML automático)
fig.write_image("messi_plot.png")

print("Gráfico PNG generado.")
