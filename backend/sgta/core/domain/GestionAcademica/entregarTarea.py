from django.db import models
from ..Autenticacion.usuario import Usuario
from ..GestionTarea.grupo import Grupo
from ..GestionTarea.asignacion import Asignacion
from django.utils import timezone

class EntregaTarea(models.Model):
    tarea = models.ForeignKey(Asignacion, on_delete=models.CASCADE, related_name='entregas')
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='entregas_tareas')
    archivo = models.FileField(upload_to='entregas/')  # Archivo subido por el estudiante
    fecha_entregada = models.DateTimeField(auto_now_add=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True, help_text='Comentarios de retroalimentación en texto')
    retroalimentacion_archivo = models.FileField(
        upload_to='retroalimentaciones/',
        null=True,
        blank=True,
        help_text='Archivo PDF con retroalimentación detallada'
    )
    fecha_retroalimentacion = models.DateTimeField(null=True, blank=True)
    grupo = models.ForeignKey(Grupo, null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Actualizar la fecha de retroalimentación cuando se agrega o modifica el archivo
        if self.retroalimentacion_archivo and not self.fecha_retroalimentacion:
            self.fecha_retroalimentacion = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-fecha_entregada']
        verbose_name = 'Entrega de tarea'
        verbose_name_plural = 'Entregas de tareas'