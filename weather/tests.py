from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import SearchHistory

class WeatherTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_weather_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather/index.html')

    def test_search_history(self):
        response = self.client.post(reverse('index'), {'city': 'Москва'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Москва')

        history_response = self.client.get(reverse('history'))
        self.assertEqual(history_response.status_code, 200)
        self.assertContains(history_response, 'Москва')
