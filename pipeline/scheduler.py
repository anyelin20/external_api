import schedule
import time
from pipeline.etl_pipeline import ejecutar_pipeline

schedule.every(10).minutes.do(ejecutar_pipeline)

while True:
    schedule.run_pending()
    time.sleep(1)


