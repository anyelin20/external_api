from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from typing import Dict, Optional
from backend.weather.database import Base  # necesario para el modelo SQL

# Modelo SQL para formulario
class Entrada(Base):
    __tablename__ = "entradas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    clima = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=False)
    imagen_url = Column(String(255), nullable=True)

# Modelos Pydantic para validación y documentación

class EntradaCreate(BaseModel):
    nombre_usuario: str
    ciudad: str
    clima: str
    descripcion: str
    imagen_url: Optional[str] = None

class WeatherResponse(BaseModel):
    ciudad: str
    pais: str
    temperatura: float
    sensacion_termica: float
    temp_min: float
    temp_max: float
    humedad: int
    presion: int
    descripcion: str
    icono: str
    nubosidad: int
    viento_velocidad: float
    viento_direccion: int
    visibilidad: int
    amanecer: str
    atardecer: str
    coordenadas: Dict[str, float]
    timestamp: str

class WeatherSimpleResponse(BaseModel):
    ciudad: str
    temperatura: float
    descripcion: str
    humedad: int
    unidades: str

class ErrorResponse(BaseModel):
    error: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    message: str


