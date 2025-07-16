from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import requests
import json
from datetime import datetime
import asyncio
import aiohttp

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

# Crear instancia de FastAPI
app = FastAPI(
    title="API del Clima - OpenWeatherMap",
    description="API REST para obtener información del clima usando OpenWeatherMap",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_weather(self, ciudad: str, units: str = "metric") -> Optional[Dict]:
        """Obtiene información del clima para una ciudad específica (async)"""
        url = f"{self.base_url}/weather"
        
        params = {
            'q': ciudad,
            'appid': self.api_key,
            'units': units,
            'lang': 'es'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise HTTPException(
                            status_code=response.status,
                            detail=f"Error de OpenWeatherMap: {response.status}"
                        )
        except asyncio.TimeoutError:
            raise HTTPException(status_code=408, detail="Timeout en la solicitud")
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
    
    async def get_weather_formatted(self, ciudad: str, units: str = "metric") -> WeatherResponse:
        """Obtiene información del clima formateada"""
        datos = await self.get_weather(ciudad, units)
        
        if not datos:
            raise HTTPException(status_code=404, detail="No se encontraron datos del clima")
        
        try:
            weather_info = WeatherResponse(
                ciudad=datos['name'],
                pais=datos['sys']['country'],
                temperatura=datos['main']['temp'],
                sensacion_termica=datos['main']['feels_like'],
                temp_min=datos['main']['temp_min'],
                temp_max=datos['main']['temp_max'],
                humedad=datos['main']['humidity'],
                presion=datos['main']['pressure'],
                descripcion=datos['weather'][0]['description'],
                icono=datos['weather'][0]['icon'],
                nubosidad=datos['clouds']['all'],
                viento_velocidad=datos.get('wind', {}).get('speed', 0),
                viento_direccion=datos.get('wind', {}).get('deg', 0),
                visibilidad=datos.get('visibility', 0),
                amanecer=datetime.fromtimestamp(datos['sys']['sunrise']).strftime('%H:%M:%S'),
                atardecer=datetime.fromtimestamp(datos['sys']['sunset']).strftime('%H:%M:%S'),
                coordenadas={
                    'latitud': datos['coord']['lat'],
                    'longitud': datos['coord']['lon']
                },
                timestamp=datetime.now().isoformat()
            )
            
            return weather_info
            
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Error al procesar datos: {str(e)}")

# Configuración
API_KEY = 'a54fc02404ab14f7755566fe1a2cafd8'
weather_api = WeatherAPI(API_KEY)

# Endpoints

@app.get("/", summary="Documentación de la API")
async def root():
    """Página de inicio con información de la API"""
    return {
        "message": "API del Clima - OpenWeatherMap",
        "version": "1.0.0",
        "documentacion": {
            "swagger_ui": "http://localhost:8000/docs",
            "redoc": "http://localhost:8000/redoc"
        },
        "endpoints": {
            "GET /": "Documentación de la API",
            "GET /weather/{ciudad}": "Obtener clima de una ciudad",
            "GET /weather/{ciudad}?format=simple": "Obtener clima simplificado",
            "GET /weather/{ciudad}?units=imperial": "Obtener clima en unidades imperiales",
            "GET /health": "Estado de la API"
        },
        "ejemplos": {
            "clima_san_jose": "http://localhost:8000/weather/San Jose,CR",
            "clima_simple": "http://localhost:8000/weather/San Jose,CR?format=simple",
            "clima_fahrenheit": "http://localhost:8000/weather/San Jose,CR?units=imperial"
        }
    }

@app.get("/weather/{ciudad}", 
         summary="Obtener clima de una ciudad",
         description="Obtiene información detallada del clima para una ciudad específica")
async def get_weather(
    ciudad: str,
    format: Optional[str] = Query(default="complete", description="Formato de respuesta: 'simple' o 'complete'"),
    units: Optional[str] = Query(default="metric", description="Unidades: 'metric', 'imperial', o 'kelvin'")
):
    """
    Obtiene el clima de una ciudad específica.
    
    - **ciudad**: Nombre de la ciudad (ej: "San Jose,CR", "Madrid,ES")
    - **format**: Tipo de respuesta (simple o complete)
    - **units**: Unidades de medida (metric, imperial, kelvin)
    """
    
    # Validar unidades
    if units not in ['metric', 'imperial', 'kelvin']:
        raise HTTPException(
            status_code=400, 
            detail="Unidades inválidas. Use: metric, imperial, o kelvin"
        )
    
    try:
        if format == "simple":
            # Formato simple
            datos = await weather_api.get_weather(ciudad, units)
            
            simple_data = WeatherSimpleResponse(
                ciudad=datos['name'],
                temperatura=datos['main']['temp'],
                descripcion=datos['weather'][0]['description'],
                humedad=datos['main']['humidity'],
                unidades=units
            )
            return simple_data
        
        else:
            # Formato completo
            datos = await weather_api.get_weather_formatted(ciudad, units)
            return datos
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.get("/health", 
         response_model=HealthResponse,
         summary="Estado de la API",
         description="Verifica el estado de funcionamiento de la API")
async def health_check():
    """Endpoint para verificar el estado de la API"""
    return HealthResponse(
        status="OK",
        timestamp=datetime.now().isoformat(),
        message="API funcionando correctamente"
    )

# Manejadores de errores personalizados
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint no encontrado"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Error interno del servidor"}

# Punto de entrada
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando FastAPI del Clima...")
    print("📍 Servidor corriendo en: http://localhost:8000")
    print("📖 Documentación Swagger: http://localhost:8000/docs")
    print("📘 Documentación ReDoc: http://localhost:8000/redoc")
    print("🔗 Ejemplo: http://localhost:8000/weather/San Jose,CR")
    print("⏹️  Presiona Ctrl+C para detener el servidor")
    
    uvicorn.run(
        "weather_api:app",  # Cambia "main" por el nombre de tu archivo
        host="0.0.0.0",
        port=8000,
        reload=True,  # Recarga automática en desarrollo
        log_level="info"
    )