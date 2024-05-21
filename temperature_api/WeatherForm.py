from django import forms

class WeatherForm(forms.Form):
    temperature = forms.FloatField(label='Temperature')
    city = forms.CharField(label='City', max_length=255)
    atmosphericPressure = forms.FloatField(label='Atmospheric Pressure', required=False)
    humidity = forms.FloatField(label='Humidity', required=False)
    weather = forms.CharField(label='Weather', max_length=255, required=False)
