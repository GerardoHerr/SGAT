from django.db import models
from ..Autenticacion.usuario import Usuario
from ..GestionAcademica.curso import Curso

class Asignacion(models.Model):
    TIPOS_TAREA = [
        ('ACD', 'Actividad de Construcción del Conocimiento'),
        ('AA', 'Actividad de Aprendizaje'),
        ('APE', 'Actividad Práctica Específica')
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_tarea = models.CharField(max_length=3, choices=TIPOS_TAREA)
    #asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, null=True, blank=True)
    es_grupal = models.BooleanField(default=False)
    fecha_entrega = models.DateTimeField()
    creada_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'DOC'}, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    activa = models.BooleanField(default=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='tareas')
    archivo_explicacion = models.FileField(upload_to='explicaciones_tareas/', null=True, blank=True, help_text='Archivo PDF con la explicación de la tarea')
    # Relaciones para asignaciones
    #estudiantes_asignados = models.ManyToManyField(Usuario, blank=True, related_name='tareas_asignadas', limit_choices_to={'rol': 'EST'})
    #grupos_asignados = models.ManyToManyField(Grupo, blank=True, related_name='tareas_asignadas')
    
    def __str__(self):
        return f"{self.titulo}"
