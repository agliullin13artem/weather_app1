from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from .form import CityForm
from .models import SearchHistory

def get_weather(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        weather_data = get_weather_data(city)  # Используйте правильное имя функции
        context = {
            'weather_data': weather_data,
            'city': city
        }
        return render(request, 'weather/index.html', context)
    return render(request, 'weather/index.html')

def get_weather_data(city):
    geocode_url = f"https://geocode.xyz/{city}?json=1"
    geocode_response = requests.get(geocode_url).json()
    latitude = geocode_response.get('latt')
    longitude = geocode_response.get('longt')

    if not latitude or not longitude:
        return None

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
    weather_response = requests.get(weather_url).json()

    if 'hourly' in weather_response and 'temperature_2m' in weather_response['hourly']:
        return weather_response
    return None

def index(request):
    weather_data = None
    city = None
    temperature = None

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather_data(city)

            if weather_data and 'hourly' in weather_data and 'temperature_2m' in weather_data['hourly']:
                temperature = weather_data['hourly']['temperature_2m'][0] if len(weather_data['hourly']['temperature_2m']) > 0 else None
            else:
                temperature = None

            search_history, created = SearchHistory.objects.get_or_create(user=request.user, city=city)
            if not created:
                search_history.search_count += 1
                search_history.save()
    else:
        form = CityForm()

    context = {
        'weather_data': weather_data,
        'city': city,
        'form': form,
        'temperature': temperature,
    }
    return render(request, 'weather/index.html', context)

@login_required
def search_history(request):
    history = SearchHistory.objects.filter(user=request.user)
    return render(request, 'weather/history.html', {'history': history})
def home(request):
    weather = None
    city = None
    if request.method == 'POST':
        city = request.POST.get('city')
        url = f'http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q={city}&aqi=no'
        response = requests.get(url)
        
        if response.status_code != 200:
            # Обработайте ошибку
            return render(request, 'weather/index.html', {'error': 'Ошибка при получении данных о погоде', 'city': city})
        
        try:
            data = response.json()
            weather = data['current']['condition']['text']
        except ValueError:
            # Обработайте ошибку декодирования
            return render(request, 'weather/index.html', {'error': 'Ошибка при декодировании данных о погоде', 'city': city})

    return render(request, 'weather/index.html', {'weather': weather, 'city': city})