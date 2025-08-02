import os
import json
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Entrada, EntradaCleaned

def ejecutar_pipeline():
    db: Session = SessionLocal()

    # EXTRAER datos de la tabla RAW (formulario)
    datos_raw = db.query(Entrada).all()
    if not datos_raw:
        return {"mensaje": "No hay datos en la tabla formulario (raw)."}

    df_raw = pd.DataFrame([r.__dict__ for r in datos_raw])
    df_raw.drop(columns=["_sa_instance_state"], inplace=True)

    total_leidos = len(df_raw)

    # TRANSFORMAR: eliminar nulos, formatear campos
    df_clean = df_raw.dropna(subset=["nombre", "ciudad", "clima"])
    df_clean["nombre"] = df_clean["nombre"].str.strip().str.title()
    df_clean["ciudad"] = df_clean["ciudad"].str.strip().str.title()
    df_clean["clima"] = df_clean["clima"].str.strip().str.lower()

    total_limpiados = total_leidos - len(df_clean)

    # CARGAR: insertar en tabla cleaned_data
    for _, row in df_clean.iterrows():
        entrada_limpia = EntradaCleaned(
            nombre=row["nombre"],
            ciudad=row["ciudad"],
            clima=row["clima"],
            descripcion=row.get("descripcion"),
            imagen=row.get("imagen")
        )
        db.add(entrada_limpia)
    db.commit()

    # BACKUP + LOG
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)

    df_raw.to_csv(f"{backup_dir}/raw_{timestamp}.csv", index=False)
    df_clean.to_csv(f"{backup_dir}/cleaned_{timestamp}.csv", index=False)

    log = {
        "timestamp": timestamp,
        "registros_leidos": total_leidos,
        "registros_limpiados": total_limpiados
    }

    with open(f"{backup_dir}/log_{timestamp}.json", "w") as f:
        json.dump(log, f, indent=4)

    return {
        "mensaje": "Pipeline ejecutado correctamente.",
        "resumen": log
    }

