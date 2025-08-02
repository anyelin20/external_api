# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.weather import router as weather_router
from pipeline.etl_pipeline import ejecutar_pipeline # n


app = FastAPI(
    title="API del Clima",
    description="API que conecta con OpenWeatherMap",
    version="1.0.0"
)

# Configuración CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir todas las rutas definidas en weather_router
app.include_router(weather_router.router)

# Para ejecutar:
# uvicorn backend.main:app --reload

#.................................................
# Endpoint manual para ejecutar pipeline # n
@app.post("/api/pipeline/run")
def correr_pipeline():
    return ejecutar_pipeline()

#Ejecutar:
#uvicorn backend.main:app --reload
#solicitud POST a: http://localhost:8000/api/pipeline/run

