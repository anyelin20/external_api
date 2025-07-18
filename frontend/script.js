// Array para almacenar las ciudades
let cities = [];

// Configuración de la API
const API_BASE_URL = 'http://localhost:8000';

// Función para agregar una nueva ciudad
async function addCity() {
    const cityInput = document.getElementById('cityInput');
    const cityName = cityInput.value.trim();
    
    if (cityName === '') {
        alert('Por favor ingresa el nombre de una ciudad');
        return;
    }

    // Verificar si la ciudad ya existe
    if (cities.find(city => city.name.toLowerCase() === cityName.toLowerCase())) {
        alert('Esta ciudad ya está en la lista');
        return;
    }

    // Mostrar estado de carga
    const addBtn = document.querySelector('.add-btn');
    const originalText = addBtn.textContent;
    addBtn.textContent = 'Agregando...';
    addBtn.disabled = true;

    try {
        // Obtener datos reales de la API
        const weatherData = await getWeatherData(cityName);
        cities.push(weatherData);
        cityInput.value = '';
        renderWeatherCards();
        
        // Mostrar mensaje de éxito
        showNotification(`✅ ${weatherData.name} agregada exitosamente`, 'success');
        
    } catch (error) {
        console.error('Error al agregar ciudad:', error);
        showNotification(`❌ Error: ${error.message}`, 'error');
    } finally {
        // Restaurar botón
        addBtn.textContent = originalText;
        addBtn.disabled = false;
    }
}

// Función para obtener datos del clima desde la API
async function getWeatherData(cityName) {
    try {
        const response = await fetch(`${API_BASE_URL}/weather_api/${encodeURIComponent(cityName)}`);
        
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Ciudad no encontrada');
            } else if (response.status === 408) {
                throw new Error('Tiempo de espera agotado');
            } else {
                throw new Error(`Error del servidor: ${response.status}`);
            }
        }
        
        const data = await response.json();
        
        // Formatear datos para el frontend
        return {
            name: data.ciudad,
            country: data.pais,
            temperature: Math.round(data.temperatura),
            description: capitalizeFirstLetter(data.descripcion),
            feelsLike: Math.round(data.sensacion_termica),
            humidity: data.humedad,
            windSpeed: data.viento_velocidad.toFixed(1),
            pressure: data.presion,
            visibility: Math.round(data.visibilidad / 1000), // Convertir de metros a kilómetros
            icon: data.icono,
            tempMin: Math.round(data.temp_min),
            tempMax: Math.round(data.temp_max),
            cloudiness: data.nubosidad,
            sunrise: data.amanecer,
            sunset: data.atardecer,
            coordinates: data.coordenadas,
            timestamp: new Date(data.timestamp).toLocaleString()
        };
        
    } catch (error) {
        if (error.name === 'TypeError') {
            throw new Error('No se pudo conectar con el servidor. Verifica que la API esté corriendo.');
        }
        throw error;
    }
}

// Función para capitalizar la primera letra
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Función para obtener icono del clima desde OpenWeatherMap
function getWeatherIcon(iconCode) {
    if (iconCode) {
        return `https://openweathermap.org/img/wn/${iconCode}@2x.png`;
    }
    return '☁️';
}

// Función para obtener emoji del clima
function getWeatherEmoji(description, iconCode) {
    const desc = description.toLowerCase();
    if (iconCode) {
        const iconMap = {
            '01d': '☀️', '01n': '🌙',
            '02d': '⛅', '02n': '⛅',
            '03d': '☁️', '03n': '☁️',
            '04d': '☁️', '04n': '☁️',
            '09d': '🌧️', '09n': '🌧️',
            '10d': '🌦️', '10n': '🌦️',
            '11d': '⛈️', '11n': '⛈️',
            '13d': '❄️', '13n': '❄️',
            '50d': '🌫️', '50n': '🌫️'
        };
        return iconMap[iconCode] || '☁️';
    }
    if (desc.includes('despejado') || desc.includes('clear')) return '☀️';
    if (desc.includes('lluvia') || desc.includes('rain')) return '🌧️';
    if (desc.includes('tormenta') || desc.includes('storm')) return '⛈️';
    if (desc.includes('nieve') || desc.includes('snow')) return '❄️';
    if (desc.includes('niebla') || desc.includes('mist')) return '🌫️';
    return '☁️';
}

// Función para obtener clase CSS del clima
function getWeatherClass(description, iconCode) {
    if (iconCode) {
        if (iconCode.includes('01') || iconCode.includes('02')) return 'sunny';
        if (iconCode.includes('09') || iconCode.includes('10') || iconCode.includes('11')) return 'rainy';
    }
    const desc = description.toLowerCase();
    if (desc.includes('clear') || desc.includes('despejado')) return 'sunny';
    if (desc.includes('rain') || desc.includes('lluvia') || desc.includes('storm')) return 'rainy';
    return 'cloudy';
}

// Función para renderizar las tarjetas del clima
function renderWeatherCards() {
    const weatherGrid = document.getElementById('weatherGrid');
    if (cities.length === 0) {
        weatherGrid.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🌤️</div>
                <div class="empty-state-text">No cities added yet</div>
                <div class="empty-state-subtext">Add a city to start tracking weather</div>
            </div>
        `;
        return;
    }
    weatherGrid.innerHTML = cities.map(city => `
        <div class="weather-card ${getWeatherClass(city.description, city.icon)}">
            <div class="weather-header">
                <div class="city-info">
                    <span class="city-name">${city.name}</span>
                    <span class="country-tag">${city.country}</span>
                </div>
                <div class="weather-icon-container">
                    <img src="${getWeatherIcon(city.icon)}" alt="${city.description}" class="weather-icon-img">
                    <span class="weather-icon-emoji">${getWeatherEmoji(city.description, city.icon)}</span>
                </div>
            </div>
            <div class="temperature-section">
                <div class="temperature">${city.temperature}°C</div>
                <div class="temp-range">
                    <span class="temp-min">${city.tempMin}°</span> / 
                    <span class="temp-max">${city.tempMax}°</span>
                </div>
            </div>
            <div class="weather-description">${city.description}</div>
            <div class="feels-like">Feels like ${city.feelsLike}°C</div>
            <div class="weather-details">
                <div class="detail-item">
                    <span class="detail-icon">💧</span>
                    <span>Humidity: ${city.humidity}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">💨</span>
                    <span>Wind: ${city.windSpeed} m/s</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">🌡️</span>
                    <span>Pressure: ${city.pressure} hPa</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">👁️</span>
                    <span>Visibility: ${city.visibility} km</span>
                </div>
            </div>
            <div class="extra-info">
                <div class="sun-times">
                    <span class="sunrise">🌅 ${city.sunrise}</span>
                    <span class="sunset">🌇 ${city.sunset}</span>
                </div>
                <div class="last-updated">
                    <small>Updated: ${city.timestamp}</small>
                </div>
            </div>
        </div>
    `).join('');
}

// Función para filtrar ciudades
function filterCities() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const temperatureFilter = document.getElementById('temperatureFilter').value;
    const weatherFilter = document.getElementById('weatherFilter').value;
    
    let filteredCities = cities;

    // Filtrar por búsqueda
    if (searchTerm) {
        filteredCities = filteredCities.filter(city => 
            city.name.toLowerCase().includes(searchTerm)
        );
    }

    // Filtrar por temperatura
    if (temperatureFilter !== 'all') {
        filteredCities = filteredCities.filter(city => {
            const temp = city.temperature;
            switch (temperatureFilter) {
                case 'hot': return temp > 25;
                case 'warm': return temp >= 15 && temp <= 25;
                case 'cold': return temp < 15;
                default: return true;
            }
        });
    }

    // Filtrar por clima
    if (weatherFilter !== 'all') {
        filteredCities = filteredCities.filter(city => {
            const desc = city.description.toLowerCase();
            switch (weatherFilter) {
                case 'clear': return desc.includes('clear') || desc.includes('despejado');
                case 'clouds': return desc.includes('cloud') || desc.includes('nube');
                case 'rain': return desc.includes('rain') || desc.includes('lluvia');
                case 'snow': return desc.includes('snow') || desc.includes('nieve');
                default: return true;
            }
        });
    }

    // Renderizar ciudades filtradas
    renderFilteredCities(filteredCities);
}

// Función para renderizar ciudades filtradas
function renderFilteredCities(filteredCities) {
    const weatherGrid = document.getElementById('weatherGrid');
    if (filteredCities.length === 0) {
        weatherGrid.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <div class="empty-state-text">No cities match your filters</div>
                <div class="empty-state-subtext">Try adjusting your search criteria</div>
            </div>
        `;
        return;
    }
    weatherGrid.innerHTML = filteredCities.map(city => `
        <div class="weather-card ${getWeatherClass(city.description, city.icon)}">
            <div class="weather-header">
                <div class="city-info">
                    <span class="city-name">${city.name}</span>
                    <span class="country-tag">${city.country}</span>
                </div>
                <div class="weather-icon-container">
                    <img src="${getWeatherIcon(city.icon)}" alt="${city.description}" class="weather-icon-img">
                    <span class="weather-icon-emoji">${getWeatherEmoji(city.description, city.icon)}</span>
                </div>
            </div>
            <div class="temperature-section">
                <div class="temperature">${city.temperature}°C</div>
                <div class="temp-range">
                    <span class="temp-min">${city.tempMin}°</span> / 
                    <span class="temp-max">${city.tempMax}°</span>
                </div>
            </div>
            <div class="weather-description">${city.description}</div>
            <div class="feels-like">Feels like ${city.feelsLike}°C</div>
            <div class="weather-details">
                <div class="detail-item">
                    <span class="detail-icon">💧</span>
                    <span>Humidity: ${city.humidity}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">💨</span>
                    <span>Wind: ${city.windSpeed} m/s</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">🌡️</span>
                    <span>Pressure: ${city.pressure} hPa</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">👁️</span>
                    <span>Visibility: ${city.visibility} km</span>
                </div>
            </div>
            <div class="extra-info">
                <div class="sun-times">
                    <span class="sunrise">🌅 ${city.sunrise}</span>
                    <span class="sunset">🌇 ${city.sunset}</span>
                </div>
                <div class="last-updated">
                    <small>Updated: ${city.timestamp}</small>
                </div>
            </div>
        </div>
    `).join('');
}

// Función para actualizar todos los datos
async function refreshAll() {
    if (cities.length === 0) {
        showNotification('No hay ciudades para actualizar', 'warning');
        return;
    }
    
    const refreshBtn = document.querySelector('.refresh-btn');
    const originalText = refreshBtn.textContent;
    refreshBtn.textContent = 'Actualizando...';
    refreshBtn.disabled = true;
    refreshBtn.classList.add('loading');
    
    try {
        // Actualizar todas las ciudades en paralelo
        const promises = cities.map(async (city, index) => {
            try {
                const updatedData = await getWeatherData(city.name);
                cities[index] = updatedData;
                return { success: true, city: city.name };
            } catch (error) {
                console.error(`Error actualizando ${city.name}:`, error);
                return { success: false, city: city.name, error: error.message };
            }
        });
        
        const results = await Promise.all(promises);
        
        // Contar éxitos y fallos
        const successful = results.filter(r => r.success).length;
        const failed = results.filter(r => !r.success).length;
        
        renderWeatherCards();
        
        if (failed === 0) {
            showNotification(`✅ ${successful} ciudades actualizadas exitosamente`, 'success');
        } else {
            showNotification(`⚠️ ${successful} exitosas, ${failed} fallidas`, 'warning');
        }
        
    } catch (error) {
        console.error('Error general en actualización:', error);
        showNotification('❌ Error al actualizar ciudades', 'error');
    } finally {
        refreshBtn.textContent = originalText;
        refreshBtn.disabled = false;
        refreshBtn.classList.remove('loading');
    }
}

// Función para limpiar todas las ciudades
function clearAllCities() {
    if (cities.length === 0) {
        showNotification('No hay ciudades para eliminar', 'warning');
        return;
    }
    
    if (confirm('¿Estás seguro de que quieres eliminar todas las ciudades?')) {
        cities = [];
        renderWeatherCards();
        showNotification('🗑️ Todas las ciudades eliminadas', 'info');
    }
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
        max-width: 300px;
    `;
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    notification.style.backgroundColor = colors[type] || colors.info;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Función para probar la conectividad con la API
async function testAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            console.log('✅ API conectada:', data);
            showNotification('🔗 API conectada correctamente', 'success');
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.error('❌ Error conectando con API:', error);
        showNotification('❌ Error conectando con API. Verifica que esté corriendo en localhost:8000', 'error');
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Probar conexión con API al cargar
    testAPIConnection();
    
    // Listener para agregar ciudad con Enter
    document.getElementById('cityInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addCity();
        }
    });

    // Listeners para filtros
    document.getElementById('searchInput').addEventListener('input', filterCities);
    document.getElementById('temperatureFilter').addEventListener('change', filterCities);
    document.getElementById('weatherFilter').addEventListener('change', filterCities);

    // Renderizar inicial (vacío)
    renderWeatherCards();
});

// Función para manejar el envío del formulario de ingreso de entradas
document.addEventListener("DOMContentLoaded", () => {
  const entradaForm = document.getElementById("entradaForm");
  if (!entradaForm) return;

  entradaForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append("nombre_usuario", entradaForm.nombre_usuario.value);
    formData.append("ciudad", entradaForm.ciudad.value);
    formData.append("clima", entradaForm.clima.value);
    formData.append("descripcion", entradaForm.descripcion.value);
    formData.append("imagen_url", entradaForm.imagen_url.value);

    const respuestaForm = document.getElementById("respuestaForm");
    respuestaForm.style.color = "green";
    respuestaForm.textContent = "Enviando...";

    try {
      const response = await fetch(`${API_BASE_URL}/entradas`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (!response.ok) {
        const errorData = await response.json();
        respuestaForm.style.color = "red";
        respuestaForm.textContent = `Error: ${errorData.detail || "No se pudo crear la entrada"}`;
        return;
      }

      const data = await response.json();
      respuestaForm.style.color = "green";
      respuestaForm.textContent = `Entrada creada con ID: ${data.entrada.id}`;
      entradaForm.reset();

    } catch (error) {
      respuestaForm.style.color = "red";
      respuestaForm.textContent = `Error de red: ${error.message}`;
    }
  });
});
