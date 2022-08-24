from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index (request):
    return HttpResponse ("¡Hola, mundo!")

def informar (request):
    return HttpResponse ("Esta es nuestra primera web realizada con DJango 2022")