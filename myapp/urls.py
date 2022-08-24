from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("acerca-de",views.informar,name="acerca")
]