# run_scheduler.py
import schedule
import time
from pipeline import ejecutar_pipeline

schedule.every(5).minutes.do(ejecutar_pipeline)

while True:
    schedule.run_pending()
    time.sleep(1)

