import schedule
import time
from pipeline.etl_pipeline import ejecutar_pipeline

def job():
    resultado = ejecutar_pipeline()
    print(f"Pipeline ejecutado: {resultado}")

schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)


