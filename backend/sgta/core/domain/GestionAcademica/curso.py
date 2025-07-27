from django.db import models
from ..Autenticacion.usuario import Usuario
from ..GestionAcademica.asignatura import Asignatura

class Curso(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    docente = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'DOC'})
    estudiantes = models.ManyToManyField(Usuario, related_name='cursos_inscritos', limit_choices_to={'rol': 'EST'})
    periodo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.asignatura.nombre} - {self.periodo}"