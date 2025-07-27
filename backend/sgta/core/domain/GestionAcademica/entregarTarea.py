from django.db import models
from ..Autenticacion.usuario import Usuario
from ..GestionTarea.grupo import Grupo
from ..GestionTarea.asignacion import Asignacion

class EntregaTarea(models.Model):
    tarea = models.ForeignKey(Asignacion, on_delete=models.CASCADE, related_name='entregas')
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='entregas_tareas')
    archivo = models.FileField(upload_to='entregas/')  # o texto si es digital
    fecha_entregada = models.DateTimeField(auto_now_add=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    grupo = models.ForeignKey(Grupo, null=True, blank=True, on_delete=models.CASCADE)