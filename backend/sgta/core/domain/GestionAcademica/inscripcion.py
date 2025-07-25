from django.db import models
from ..Autenticacion.usuario import Usuario
from .asignatura import Asignatura

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'EST'},
        related_name='inscripciones_estudiante'
    )
    asignatura = models.ForeignKey(
        Asignatura, 
        on_delete=models.CASCADE,
        related_name='inscripciones_asignatura'
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('estudiante', 'asignatura')
    
    def __str__(self):
        return f"{self.estudiante.nombre} - {self.asignatura.nombre}"
