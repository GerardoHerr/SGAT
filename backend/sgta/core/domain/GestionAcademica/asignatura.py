from django.db import models
from ..Autenticacion.usuario import Usuario

class Asignatura(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)  # estado
    
    registrada_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='asignaturas_registradas')
    docente_responsable = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'rol': 'DOC'}, 
        related_name='asignaturas_responsable',
        help_text='Docente responsable de impartir la asignatura'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"