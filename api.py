import requests

# Tu API Key
API_KEY = 'a54fc02404ab14f7755566fe1a2cafd8'
# Ciudad a consultar
ciudad = 'San Jose,CR'
# URL de la API
url = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric'

# Hacer la solicitud
response = requests.get(url)

# Convertir a JSON
datos = response.json()
datos
# Extraer valores
temp = datos['main']['temp']
descripcion = datos['weather'][0]['description']
humedad = datos['main']['humidity']

print(f"Temperatura: {temp}°C")
print(f"Descripción: {descripcion}")
print(f"Humedad: {humedad}%")