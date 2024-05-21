from typing import Any
from django.utils import timezone
from datetime import datetime
from random import randrange
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from user.authenticationUser import *
from .weatherModel import WeatherEntity
from .weatherRepository import WeatherRepository
from .weatherSerializer import WeatherSerializer
from .weatherForm import WeatherForm
from .weatherExceptions import WeatherException

class WeatherView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'token' in request.session:
            token = request.session['token']
            error_code, _ = verifyToken(token)
            if error_code == 0:
                user = getAuthenticatedUser(token)
                if user:
                    request.authenticate = True
                    request.user_id = user.id  # Adicione o id do usuário à requisição
                    kwargs['user_id'] = user.id  # Adicione o user_id aos kwargs
                    return super().dispatch(request, *args, **kwargs)

        return HttpResponse('Unauthorized', status=401)

    def get(self, request, *args, **kwargs):
        if not getattr(request, 'authenticate', False):
            return HttpResponse('Unauthorized', status=401)

        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.getAll())
            serializer = WeatherSerializer(data=weathers, many=True)
            if serializer.is_valid():
                modelWeather = serializer.save()
                objectReturn = {"weathers": modelWeather, "user_id": request.user_id}  # Passa o id do usuário para o contexto do template
            else:
                objectReturn = {"error": serializer.errors, "user_id": request.user_id}  # Passa o id do usuário para o contexto do template
        except WeatherException as e:
            objectReturn = {"error": e.message, "user_id": request.user_id}  # Passa o id do usuário para o contexto do template

        return render(request, "home_weather.html", objectReturn)


class WeatherGenerate(View):

    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weather = WeatherEntity(
            temperature=randrange(start=17, stop=40),
            date=datetime.now(),
            city='Sorocaba'
        )
        serializer = WeatherSerializer(data=weather.__dict__)
        if (serializer.is_valid()):
            repository.insert(serializer.data)
        else:
            print(serializer.errors)

        return redirect('Weather View')
    
class WeatherReset(View):

    def get(self, request, user_id):  # Adicione user_id como parâmetro
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteAll()

        return redirect('Weather View', user_id=user_id)  # Passa user_id ao redirecionar
    
class WeatherInsert(View):

    def get(self, request, user_id):  # Adicione user_id como parâmetro
        weatherForm = WeatherForm()
        return render(request, "create_weather.html", {"form": weatherForm, "user_id": user_id})  # Passa user_id para o contexto do template

    def post(self, request, user_id):  # Adicione user_id como parâmetro
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            weather_data = weatherForm.cleaned_data
            weather_data['date'] = timezone.now()

            serializer = WeatherSerializer(data=weather_data)
            if serializer.is_valid():
                repository = WeatherRepository(collectionName='weathers')
                repository.insert(serializer.data)
                return redirect('Weather View', user_id=user_id)  # Passa user_id ao redirecionar
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect('Weather View', user_id=user_id)  # Passa user_id ao redirecionar

    

class WeatherEdit(View):

    def get(self, request, id, user_id):  # Adicione user_id como parâmetro
        repository = WeatherRepository(collectionName='weathers')
        weather = repository.getByID(id)
        initial_data = {
            'temperature': weather['temperature'],
            'city': weather['city'],
            'atmosphericPressure': weather.get('atmosphericPressure', 0),
            'humidity': weather.get('humidity', 0),
            'weather': weather.get('weather', ''),
            'date': weather['date']  # Adiciona a data do objeto ao formulário
        }
        weatherForm = WeatherForm(initial=initial_data)

        return render(request, "form_edit_weather.html", {"form": weatherForm, "id": id, "user_id": user_id})  # Passa user_id para o contexto do template

    def post(self, request, id, user_id):  # Adicione user_id como parâmetro
        repository = WeatherRepository(collectionName='weathers')
        weather = repository.getByID(id)
        weatherForm = WeatherForm(request.POST, initial=weather)

        if weatherForm.is_valid():
            weather_data = {
                'temperature': weatherForm.cleaned_data['temperature'],
                'city': weatherForm.cleaned_data['city'],
                'atmosphericPressure': weatherForm.cleaned_data.get('atmosphericPressure', 0),
                'humidity': weatherForm.cleaned_data.get('humidity', 0),
                'weather': weatherForm.cleaned_data.get('weather', ''),
            }
            # Adiciona a data apenas se não estiver presente nos dados do formulário
            if 'date' not in request.POST:
                weather_data['date'] = timezone.now()
            serializer = WeatherSerializer(data=weather_data)
            if serializer.is_valid():
                repository.update(serializer.data, id)
                return redirect('Weather View', user_id=user_id)  # Passa user_id ao redirecionar
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect('Weather View', user_id=user_id)  # Passa user_id ao redirecionar


class WeatherDelete(View):
    
    def get(self, request, id, user_id):  # Adicione user_id como parâmetro
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteByID(id)

        return redirect('Weather View', user_id=user_id)  # Passa user_id ao redirecionar


class WeatherFilter(View):
    def post(self, request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.get(data))
            serializer = WeatherSerializer(data=weathers, many=True)
            if (serializer.is_valid()):
                modelWeather = serializer.save()
                objectReturn = {"weathers":modelWeather}
            else:
                objectReturn = {"error":serializer.errors}
        except WeatherException as e:
            objectReturn = {"error":e.message}
  
        return render(request, "home_weather.html", objectReturn)