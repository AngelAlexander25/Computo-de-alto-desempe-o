import pandas as pd
import json
import os

# Script para convertir el CSV de datos de Messi a JSON para usar en el dashboard web

# Función para convertir CSV a JSON
def convert_csv_to_json():
    print("Convirtiendo datos de Messi a formato JSON...")
    
    try:
        # Leer el archivo CSV (utilizando el encoding correcto)
        df = pd.read_csv('messi_barca.csv', encoding='cp1252')
        
        # Mostrar información sobre el dataframe
        print(f"Archivo CSV cargado. Dimensiones: {df.shape}")
        print("\nPrimeras 5 filas:")
        print(df.head())
        
        # Verificar la estructura de columnas
        print("\nColumnas encontradas:")
        print(df.columns.tolist())
        
        # Convertir columnas a tipos adecuados
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
        
        # Asegurar que las columnas de texto sean string
        string_columns = ['Season', 'Competition']
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype(str)
        
        # Rellenar valores NaN
        fill_values = {
            'Competition': 'No Competition',
            'Matches Played': 0,
            'Starts': 0,
            'Minutes played': 0,
            'Goals scored': 0,
            'Assists': 0,
            'PK': 0,
            'PKatt': 0,
            'CrdY': 0,
            'CrdR': 0,
            'Goal/90': 0.0,
            'Ast/90': 0.0,
            'G+A/90': 0.0,
            'G-PK/90': 0.0,
            'G+A-PK/90': 0.0
        }
        
        for col, value in fill_values.items():
            if col in df.columns:
                df[col] = df[col].fillna(value)
        
        # Convertir a JSON
        json_data = df.to_json(orient='records')
        parsed_data = json.loads(json_data)
        
        # Guardar a archivo JSON con formato legible
        with open('messi_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(parsed_data, json_file, indent=4, ensure_ascii=False)
        
        print(f"\nArchivo JSON creado exitosamente: messi_data.json")
        print(f"Contiene {len(parsed_data)} registros.")
        
        # Verificar que funcione correctamente leyendo el archivo
        with open('messi_data.json', 'r', encoding='utf-8') as json_file:
            test_data = json.load(json_file)
            print(f"Verificación: Se pueden leer {len(test_data)} registros del archivo JSON.")
        
        return True
        
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        return False

# Ejecutar la conversión
if __name__ == "__main__":
    convert_csv_to_json()