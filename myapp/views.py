from pydoc import Helper
import sqlite3
import requests
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import virtualenv
from . import forms
from .models import Curso



def index(request):
    html = """
    <html>
        <h1>
            Hola : 
        </h1> 
        <br>
        <h3>
            Este proyecto contempla todo lo visto hasta el 26/09 sin modificar, ni borrar, siempre agregando. 
            Asi les queda un resumen. &#128512;
        </h3> 
    </html>
    """
    return HttpResponse(html)


def acerca_de(request):
    return HttpResponse("¡Curso de Python y Django!")


def cursos_json(request):
    conn = sqlite3.connect("cursos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM cursos")
    response = JsonResponse(cursor.fetchall(), safe=False)
    conn.close()
    return response


def cursos(request):
    conn = sqlite3.connect("cursos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM cursos")
    html = """
        <html>
        <title>Lista de cursos</title>
        <table style="border: 1px solid">
          <thead>
            <tr>
              <th>Curso</th>
              <th>Inscriptos</th>
            </tr>
          </thead>
    """
    # python 10
    # java  12
    # php 8
    # [("python",10),("java",12),("php",8)]
    # (nombre, inscriptos)

    # html = algo
    # html = algo + otra cosa
    for nombre, inscriptos in cursor.fetchall():
        html += f"""
            <tr>
              <td>{nombre}</td>
              <td>{inscriptos}</td>
            </tr>
        """
    html += "</table></html>"
    conn.close()
    return HttpResponse(html)


def cotizacion_dolar(request):
    r = requests.get(
        "https://api-dolar-argentina.herokuapp.com/api/dolaroficial")
    resultado = r.json()
    html = f"""
        <html>
        <title>Cotización del dólar</title>
        <p><strong>Compra</strong>: {resultado["compra"]}</p>
        <p><strong>Venta</strong>: {resultado["venta"]}</p>
        </html>
    """
    return HttpResponse(html)


def aeropuertos(request):
    f = open("aeropuertos.csv", encoding="utf8")
    html = """
        <html>
        <title>Lista de aeropuertos</title>
        <table style="border: 1px solid">
          <thead>
            <tr>
              <th>Aeropuerto</th>
              <th>Ciudad</th>
              <th>País</th>
            </tr>
          </thead>
    """
    for linea in f:
        datos = linea.split(",")
        nombre = datos[1].replace('"', "")
        ciudad = datos[2].replace('"', "")
        pais = datos[3].replace('"', "")
        html += f"""
            <tr>
              <td>{nombre}</td>
              <td>{ciudad}</td>
              <td>{pais}</td>
            </tr>
        """
    f.close()
    html += "</table></html>"
    return HttpResponse(html)


def aeropuertos_json(request):
    f = open("aeropuertos.csv", encoding="utf8")
    aeropuertos = []
    for linea in f:
        datos = linea.split(",")
        aeropuerto = {
            "nombre": datos[1].replace('"', ""),
            "ciudad": datos[2].replace('"', ""),
            "pais": datos[3].replace('"', "")
        }
        aeropuertos.append(aeropuerto)
    f.close()
    return JsonResponse(aeropuertos, safe=False)


def nuevo_index(request):
    ctx = {"nombre": "Juan", "cursos": 5, "actualmente": "Django"}
    return render(request, "myapp/index.html", ctx)


def nuevos_cursos(request):
    conn = sqlite3.connect("cursos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM cursos")
    cursos = cursor.fetchall()
    conn.close()
    ctx = {"cursos": cursos}
    return render(request, "myapp/cursos.html", ctx)


def curso(request, nombre_curso):
    conn = sqlite3.connect("cursos.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, inscriptos FROM cursos WHERE nombre=?", [nombre_curso])
    curso = cursor.fetchone()
    ctx = {"curso": curso}
    conn.close()

    return render(request, "myapp/curso.html", ctx)


"""
def nuevo_curso(request):
    form = forms.FormularioCurso()
    ctx = {"form": form}
    return render(request, "myapp/nuevo_curso.html", ctx)
"""


def nuevo_curso(request):
    if request.method == "POST":
        form = forms.FormularioCurso(request.POST)
        if form.is_valid():
            conn = sqlite3.connect("cursos.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cursos VALUES (?, ?)",
                (form.cleaned_data["nombre"], form.cleaned_data["inscriptos"]))
            conn.commit()
            conn.close()
            return HttpResponse("¡Curso creado correctamente!")
    else:
        form = forms.FormularioCurso()
        ctx = {"form": form}
        return render(request, "myapp/nuevo_curso.html", ctx)



#Esta view esta vinculada con la url imagen, no darle importancia, es solo 
#para que vean como se configura una base de datos distinta a sqlite
def muestra(request):
    return render(request, "myapp/imagen_muestra.html")


# Esta view esta vinculada con la url vista-curso , generada con el template vista_curso.html
# Esto es lo que hicimos 12/09, junto con el manejo del shell de Django y junto con 
# lo que vimos de modelos, migraciones y ORM
def cursos_orm(request):
    ctx ={"cursos": Curso.objects.all() }
    return render(request, "myapp/vista_curso.html", ctx)



# Esta view esta vinculada con la url new-curso , generada con el template new_curso.html
# para armar el formulario a partir del modelo. Esto es lo que hicimos 19/09, junto con
# la teoria de tipos de datos, agregar campos a tablas, filtros y vinculación a los formularios.
# tambien mirar forms.py que esta el formulario armado a partir del modelo. 
def new_curso(request):
    if request.method == "POST":
        form = forms.FormularioCursoDos(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("cursos_orm"))
    else:
        form = forms.FormularioCursoDos()
    ctx = {"form": form}
    return render(request, "myapp/new_curso.html", ctx)