# pipeline.py
import pymysql
import pandas as pd
from datetime import datetime
import os
import json

def conectar_db():
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="123Queso",
        database="weather_app",
        cursorclass=pymysql.cursors.DictCursor
    )

def extraer_datos():
    conn = conectar_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM raw_data")
        rows = cursor.fetchall()
    return pd.DataFrame(rows)

def transformar(df):
    original = len(df)

    df = df.dropna()  # eliminar nulos
    df['ciudad'] = df['ciudad'].str.title().str.strip()
    df['nombre'] = df['nombre'].str.title().str.strip()
    df['clima'] = df['clima'].str.lower().str.strip()
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df.dropna(subset=['fecha'])  # eliminar fechas inválidas

    limpiados = original - len(df)
    return df, limpiados

def cargar(df):
    conn = conectar_db()
    with conn.cursor() as cursor:
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO cleaned_data (nombre, ciudad, clima, descripcion, fecha, imagen_url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['nombre'], row['ciudad'], row['clima'], row['descripcion'], row['fecha'], row['imagen_url']))
    conn.commit()

def backup(df_raw, df_cleaned):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("backups", exist_ok=True)

    raw_path = f"backups/raw_{timestamp}.csv"
    clean_path = f"backups/cleaned_{timestamp}.csv"
    log_path = f"backups/log_{timestamp}.json"

    df_raw.to_csv(raw_path, index=False)
    df_cleaned.to_csv(clean_path, index=False)

    log = {
        "timestamp": timestamp,
        "registros_leidos": len(df_raw),
        "registros_limpiados": len(df_raw) - len(df_cleaned),
        "csv_raw": raw_path,
        "csv_cleaned": clean_path
    }

    with open(log_path, "w") as f:
        json.dump(log, f, indent=4)

def ejecutar_pipeline():
    df_raw = extraer_datos()
    df_clean, eliminados = transformar(df_raw)
    cargar(df_clean)
    backup(df_raw, df_clean)
    return {
        "leidos": len(df_raw),
        "eliminados": eliminados,
        "almacenados": len(df_clean)
    }

# manualmente:
if __name__ == "__main__":
    resultado = ejecutar_pipeline()
    print(resultado)

