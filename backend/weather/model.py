from pydantic import BaseModel
from typing import Dict
from typing import Optional

# Modelos Pydantic para validación y documentación
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
