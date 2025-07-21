from django.db import models
from ..Autenticacion.usuario import Usuario

class Asignatura(models.Model):
    ESTADO_ASIGNATURA = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
    ]
    
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_ASIGNATURA,
        default='activa'
    )
    
    #registrada_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"