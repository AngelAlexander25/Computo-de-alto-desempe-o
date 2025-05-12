import pandas as pd
import plotly.express as px

# Leer dataset
df = pd.read_csv("messi-barca.csv")
df['Temporada'] = df['Temporada'].astype(str)
df['Goles'] = pd.to_numeric(df['Goles'], errors='coerce')

# Crear gráfico
fig = px.bar(df, x='Temporada', y='Goles', title='Goles de Messi por Temporada en el Barcelona')

# Guardar como imagen
fig.write_image("messi_plot.png")

print("Gráfico PNG generado.")
