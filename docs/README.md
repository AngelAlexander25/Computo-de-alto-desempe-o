# Visualización de Estadísticas de Messi con Elasticsearch

Este proyecto proporciona una solución sencilla para visualizar las estadísticas de Lionel Messi en el FC Barcelona utilizando Elasticsearch como base de datos y generando gráficas estáticas que se muestran en una página HTML simple.

## Archivos del Proyecto

1. **`cargar_datos_elasticsearch.py`**: Script para cargar los datos desde el archivo CSV a Elasticsearch.
2. **`generar_graficas_messi.py`**: Script para generar las gráficas y la página HTML a partir de los datos en Elasticsearch.
3. **`requisitos.txt`**: Lista de dependencias de Python necesarias para ejecutar los scripts.
4. **`messi_barca.csv`**: Archivo CSV con las estadísticas de Messi (tu archivo original).

## Requisitos

- Python 3.x
- Conexión a Elasticsearch (cloud o servidor local)
- Paquetes de Python especificados en `requisitos.txt`

## Instrucciones de Uso

### 1. Instalación de Dependencias

Primero, instala las dependencias necesarias:

```bash
pip install -r requisitos.txt
```

### 2. Configuración de Elasticsearch

Edita los scripts `cargar_datos_elasticsearch.py` y `generar_graficas_messi.py` para actualizar los parámetros de conexión a tu instancia de Elasticsearch:

```python
# Modificar estos valores con tus credenciales
es = Elasticsearch(
    cloud_id="tu_cloud_id",
    basic_auth=("tu_usuario", "tu_contraseña")
)
```

### 3. Carga de Datos a Elasticsearch

Ejecuta el script para cargar los datos:

```bash
python cargar_datos_elasticsearch.py
```

El script:
- Cargará el archivo CSV
- Limpiará y convertirá los datos
- Creará un índice en Elasticsearch llamado `messi_stats`
- Cargará todos los registros en el índice

### 4. Generación de Gráficas

Ejecuta el script para generar las gráficas y la página HTML:

```bash
python generar_graficas_messi.py
```

El script:
- Obtendrá los datos desde Elasticsearch
- Generará 5 gráficas diferentes
- Creará una página HTML simple con las gráficas
- Guardará todo en el directorio `graficas_messi`

### 5. Visualización de Resultados

Abre el archivo HTML generado:

```bash
graficas_messi/index.html
```

## Gráficas Generadas

1. **Goles por temporada**: Muestra la evolución de goles de Messi a lo largo de las temporadas.
2. **Goles por competición**: Muestra el total de goles en cada competición.
3. **Relación entre goles y asistencias**: Gráfico de dispersión que relaciona goles y asistencias por competición.
4. **Evolución de goles y asistencias**: Muestra la tendencia de goles y asistencias a lo largo del tiempo.
5. **Goles por edad**: Muestra el rendimiento goleador de Messi según su edad.

## Notas Importantes

- Los scripts incluyen manejo de errores básico
- Asegúrate de tener los permisos correctos para tu instancia de Elasticsearch
- La página HTML generada es estática y no requiere servidor web; puede abrirse directamente en el navegador

## Personalización

- Puedes modificar el estilo de las gráficas editando los parámetros de matplotlib en `generar_graficas_messi.py`
- El diseño de la página HTML puede personalizarse editando la variable `html_content` en el mismo script
- Para añadir más gráficas, agrega nuevas secciones al script y actualiza el HTML correspondiente