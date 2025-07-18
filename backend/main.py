# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from weather import router as weather_router

app = FastAPI(
    title="API del Clima",
    description="API que conecta con OpenWeatherMap",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Rutas
app.include_router(weather_router.router)

# Uvicorn para ejecutar: uvicorn backend.main:app --reload
