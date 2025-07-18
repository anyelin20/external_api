# 🌦 Proyecto API del Clima - FastAPI + MySQL

Este proyecto es una API desarrollada con FastAPI que obtiene información del clima desde OpenWeatherMap y permite almacenar registros meteorológicos en una base de datos MySQL local. Los datos se pueden enviar y consultar mediante endpoints POST y GET.

---

## 📁 Estructura del Proyecto

EXTERNAL_API/  
├── archivos_db/  
│   └── weather_app_weather_data.sql ← script para crear la base de datos y tabla  
├── backend/  
│   ├── .venv/ ← el entorno virtual debe crearse aquí  
│   ├── main.py  
│   ├── api.py  
│   ├── weather_api.py  
│   ├── database.py ← conexión a MySQL  
│   ├── requirements.txt ← estará aquí  
│   └── weather/  
│       ├── model.py  
│       ├── router.py  
├── .gitignore  
└── README.md

---

## ⚙️ Requisitos

- Python 3.10 o superior  
- MySQL 5.7 o superior  
- Cuenta en OpenWeatherMap

---

## 🚀 Configuración del entorno

1. Abre una terminal y navega a la carpeta `backend`:

```bash
cd backend
```

2. Crea un entorno virtual:

```bash
python -m venv .venv
```

3. Activa el entorno virtual:

- En Windows:

```bash
.\.venv\Scripts\activate
```

- En Mac/Linux:

```bash
source .venv/bin/activate
```

4. Instala las dependencias desde `requirements.txt` (este archivo estará dentro de `backend/`):

```bash
pip install -r requirements.txt
```

---

## 🧪 Configurar base de datos MySQL

1. Abre **MySQL Workbench** o tu cliente favorito  
2. Ejecuta el script que se encuentra en:

```
archivos_db/weather_app_weather_data.sql
```

Este script creará la base de datos `weather_app` y la tabla `weather_data`.

---

## ▶️ Ejecutar el servidor

1. Asegúrate de estar en la carpeta `backend/`  
2. Activa el entorno virtual  
3. Ejecuta el siguiente comando:

```bash
uvicorn main:app --reload
```

Esto iniciará el servidor en:

```
http://127.0.0.1:8000
```

---

## 🧭 Endpoints disponibles

| Método | Ruta       | Descripción                                 |
|--------|------------|---------------------------------------------|
| POST   | /weather   | Guarda un registro del clima en la base     |
| GET    | /weather   | Lista todos los registros guardados         |

---

## 🧪 Swagger UI

Puedes probar los endpoints desde la interfaz web en:

```
http://127.0.0.1:8000/docs
```

---

## 🧊 Autor

Proyecto grupal desarrollado para el curso de Aplicaciones Web.
