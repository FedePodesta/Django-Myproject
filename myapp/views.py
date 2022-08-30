import sqlite3
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("<html>¡<strong>Hola</strong>, <em>mundo</em>!</html>")


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
    for (nombre, inscriptos) in cursor.fetchall():
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
    r = requests.get("https://api.recursospython.com/dollar")
    resultado = r.json()
    html = f"""
        <html>
        <title>Cotización del dólar</title>
        <p><strong>Compra</strong>: {resultado["buy_price"]}</p>
        <p><strong>Venta</strong>: {resultado["sale_price"]}</p>
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
    ctx = {"nombre":"Juan"}
    return render(request, "myapp/index.html",ctx)