from django.db import models
from django.utils import timezone
from ..Autenticacion.usuario import Usuario

class Calificacion(models.Model):
    """
    Modelo para almacenar las calificaciones de las tareas de los estudiantes.
    """
    estudiante = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='calificaciones_estudiante'
    )
    tarea = models.ForeignKey(
        'Asignacion',  # Usamos string para evitar dependencia circular
        on_delete=models.CASCADE,
        related_name='calificaciones_tarea'
    )
    calificacion = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Puntuación numérica de la tarea"
    )
    retroalimentacion = models.TextField(
        blank=True, 
        null=True,
        help_text="Comentarios o retroalimentación sobre la tarea"
    )
    calificado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='calificaciones_realizadas',
        help_text="Usuario que realizó la calificación"
    )
    fecha_calificacion = models.DateTimeField(
        default=timezone.now,
        help_text="Fecha y hora en que se realizó la calificación"
    )

    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        unique_together = (('estudiante', 'tarea'),)
        ordering = ['-fecha_calificacion']

    def __str__(self):
        return f"{self.estudiante} - {self.tarea}: {self.calificacion}"

    def save(self, *args, **kwargs):
        # Validar que el estudiante esté asignado a la tarea
        if not self.tarea.estudiantes.filter(pk=self.estudiante.pk).exists():
            raise ValueError("El estudiante no está asignado a esta tarea")
        super().save(*args, **kwargs)
