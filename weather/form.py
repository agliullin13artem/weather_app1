from django import forms

class CityForm(forms.Form):
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off', 'placeholder': 'Введите название города'}))