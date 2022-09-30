from django import forms

from django.forms import ModelForm
from .models import Curso


class FormularioCurso(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=128)
    inscriptos = forms.IntegerField(label="Inscriptos")


class FormularioCursoDos(ModelForm):
    class Meta:
        model = Curso
        fields = ("nombre", "inscriptos", "turno")