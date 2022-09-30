from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("acerca-de", views.acerca_de, name="acerca_de"),
    path("cursos", views.cursos, name="cursos"),
    path("cursos-json", views.cursos_json, name="cursos_json"),
    path("cotizacion-dolar", views.cotizacion_dolar, name="cotizacion_dolar"),
    path("aeropuertos", views.aeropuertos, name="aeropuertos"),
    path("aeropuertos/json", views.aeropuertos_json, name="aeropuertos_json"),
    path("nuevo-index", views.nuevo_index, name="nuevo_index"),
    path("nuevos-cursos", views.nuevos_cursos, name="nuevos_cursos"),
    path("curso/<str:nombre_curso>", views.curso, name="curso"),
    path("agregar-curso", views.nuevo_curso, name="agregar"),
    path("imagen",views.muestra,name="muestra"),
    path("vista-curso",views.cursos_orm,name="cursos_orm"),
    path("new-curso",views.new_curso,name="new_curso")
]
