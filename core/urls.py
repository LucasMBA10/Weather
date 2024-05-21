"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from temperature_api.weatherView import *
from user.userView import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('weather/<str:user_id>/', WeatherView.as_view(), name='Weather View'),
    path('weather/insert/<str:user_id>/', WeatherInsert.as_view(), name='Weather Insert'),
    path('weather/filter/<str:user_id>/', WeatherFilter.as_view(), name='Weather Filter'),
    path('weather/edit/<id>/<str:user_id>/', WeatherEdit.as_view(), name='Weather Edit'),
    path('weather/delete/<id>/<str:user_id>/', WeatherDelete.as_view(), name='Weather Delete'),
    path('weather/generate/<str:user_id>/', WeatherGenerate.as_view(), name='Weather Generate'),
    path('weather/reset/<str:user_id>/', WeatherReset.as_view(), name='Weather Reset'),
    path('user/token', UserToken.as_view(), name='User Token'),
    path('', UserLogin.as_view(), name='User Login'),
    path('user/insert', UserInsert.as_view(), name='User Insert'),
    path('user/forget', UserForget.as_view(), name="User Forget"),
    path('user/edit/<str:user_id>/', UserEdit.as_view(), name='User Edit'),
    path('user/delete/<str:user_id>/', UserDelete.as_view(), name='User Delete'),
]