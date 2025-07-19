import requests

API_KEY = 'a54fc02404ab14f7755566fe1a2cafd8'
ciudad = 'San Jose,CR'
url = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric'

try:
    response = requests.get(url)
    response.raise_for_status()  # Para detectar errores HTTP

    datos = response.json()

    # Verificar que existan las claves esperadas
    temp = datos['main']['temp']
    descripcion = datos['weather'][0]['description']
    humedad = datos['main']['humidity']

    print(f"Temperatura: {temp}°C")
    print(f"Descripción: {descripcion}")
    print(f"Humedad: {humedad}%")

except requests.exceptions.HTTPError as http_err:
    print(f"Error HTTP: {http_err}")
except KeyError:
    print("No se encontraron datos esperados en la respuesta.")
except Exception as err:
    print(f"Ocurrió un error: {err}")
