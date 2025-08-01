# pipeline/etl_pipeline.py

import pymysql
import pandas as pd

# Configuración de conexión a MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123Queso",
    "database": "weather_app",
    "cursorclass": pymysql.cursors.DictCursor
}

def connect():
    return pymysql.connect(**DB_CONFIG)

def extract_raw_data():
    """Extrae los datos de la tabla weather_data_raw y los devuelve como DataFrame"""
    connection = connect()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM weather_data_raw;")
        raw_data = cursor.fetchall()
    connection.close()

    df = pd.DataFrame(raw_data)
    print(f"✔ Se extrajeron {len(df)} registros de weather_data_raw.")
    return df

# Solo para pruebas locales
if __name__ == "__main__":
    df_raw = extract_raw_data()
    print(df_raw.head())

