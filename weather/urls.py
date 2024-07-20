from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Убедитесь, что это правильное представление
    path('get_weather/', views.get_weather, name='get_weather'),  # Убедитесь, что функция существует
]