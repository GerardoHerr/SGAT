from django.db import models
from datetime import datetime

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default="")
    fecha_creacion = models.DateTimeField(default=datetime.now)
    activo = models.BooleanField(default=True)
    
    # Relación con estudiantes (muchos a muchos)
    estudiantes = models.ManyToManyField('Usuario', limit_choices_to={'rol': 'Estudiante'}, blank=True)
    
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        ordering = ['nombre']
    
    def agregar_estudiante(self, estudiante) -> bool:
        # Agrega un estudiante al grupo
        if not self.estudiantes.filter(id=estudiante.id).exists():
            self.estudiantes.add(estudiante)
            return True
        return False
    
    def remover_estudiante(self, estudiante) -> bool:
        # Remueve un estudiante del grupo
        if self.estudiantes.filter(id=estudiante.id).exists():
            self.estudiantes.remove(estudiante)
            return True
        return False
    
    def tiene_estudiante(self, estudiante) -> bool:
        # Verifica si el estudiante está en el grupo
        if hasattr(estudiante, 'id'):
            return self.estudiantes.filter(id=estudiante.id).exists()
        return self.estudiantes.filter(id=estudiante).exists()
    
    def cantidad_estudiantes(self) -> int:
        # Total de estudiantes en el grupo
        return self.estudiantes.count()
    
    def esta_vacio(self) -> bool:
        # Verifica si el grupo está vacío
        return self.estudiantes.count() == 0
    
    def desactivar(self) -> bool:
        # Desactiva el grupo
        self.activo = False
        self.save()
        return True
    
    def activar(self) -> bool:
        # Activa el grupo
        self.activo = True
        self.save()
        return True
    
    def obtener_estudiantes_ids(self) -> list:
        # Retorna lista de IDs de estudiantes
        return list(self.estudiantes.values_list('id', flat=True))
    
    def __str__(self):
        return f"Grupo {self.nombre} ({self.cantidad_estudiantes()} estudiantes)"
