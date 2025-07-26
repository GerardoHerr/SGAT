from django.db import models
from ..Autenticacion.usuario import Usuario
from .asignatura import Asignatura
from .periodo_lectivo import PeriodoLectivo

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'EST'})
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    periodo_lectivo = models.ForeignKey(PeriodoLectivo, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['estudiante', 'asignatura', 'periodo_lectivo']
    
    def __str__(self):
        return f"{self.estudiante.nombre} - {self.asignatura.nombre}"
