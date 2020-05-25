from django.urls import path
from .views import Compilador, Validar

urlpatterns = [
    path('', Compilador, name='compilador'),
    path('validar', Validar, name='validar')
]