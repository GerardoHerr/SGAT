from django.db import models

class CursoReporte(models.Model):
    curso_nombre = models.CharField(max_length=200)
    periodo = models.CharField(max_length=100)
    docente_nombre = models.CharField(max_length=200)
    total_estudiantes = models.PositiveIntegerField(default=0)
    total_tareas = models.PositiveIntegerField(default=0)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.curso_nombre} - {self.periodo}"

class TareaReporte(models.Model):
    curso = models.ForeignKey(CursoReporte, related_name='tareas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()
    tipo = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('grupal', 'Grupal')])
    estado = models.CharField(max_length=20, choices=[('abierta', 'Abierta'), ('cerrada', 'Cerrada')])
    promedio_calificacion = models.FloatField(blank=True, null=True)
    porcentaje_entregas = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class EntregaReporte(models.Model):
    tarea = models.ForeignKey(TareaReporte, related_name='entregas', on_delete=models.CASCADE)
    estudiante_nombre = models.CharField(max_length=200)
    estudiante_email = models.EmailField()
    entregada = models.BooleanField(default=False)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    calificacion = models.FloatField(blank=True, null=True)
    retroalimentacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.estudiante_nombre} - {self.tarea.titulo}"
