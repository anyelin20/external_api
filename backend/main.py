# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from weather import router as weather_router

app = FastAPI(
    title="API del Clima",
    description="API que conecta con OpenWeatherMap",
    version="1.0.0"
)

# Configuración CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto si quieres restringir orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incluir todas las rutas definidas en weather_router
app.include_router(weather_router.router)

# Para ejecutar:
# uvicorn backend.main:app --reload
