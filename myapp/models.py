from django.db import models


class Profesor(models.Model):
    nombre = models.CharField(max_length=128)
    monotributista = models.BooleanField()
    class Meta: 
        verbose_name = "Profesor" 
        verbose_name_plural = "Profesores" 
        
    def __str__(self):
        return self.nombre


class Curso(models.Model):
    nombre = models.CharField(max_length=128)
    inscriptos = models.IntegerField()
    TURNOS = ( (1, "Mañana"),(2, "Tarde"),(3, "Noche"))
    turno = models.PositiveSmallIntegerField("Turno", choices=TURNOS,default=3)
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, related_name="cursos")
    class Meta: 
        verbose_name = "Curso" 
        verbose_name_plural = "Cursos"  

    def __str__(self):
        return self.nombre



