from django.db import models
from django.contrib.auth.models import AbstractUser

# Usuario
class Usuario(models.Model):
    ROLES = [
        ('ADM', 'Administrador'),
        ('DOC', 'Docente'),
        ('EST', 'Estudiante')
    ]
    
    email = models.EmailField(unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=255)  # Campo para la contraseña
    rol = models.CharField(max_length=3, choices=ROLES)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

# Asignatura
class Asignatura(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    
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

# Periodo Lectivo
class PeriodoLectivo(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class Curso(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    docente = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'DOC'})
    estudiantes = models.ManyToManyField(Usuario, related_name='cursos_inscritos', limit_choices_to={'rol': 'EST'})
    periodo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.asignatura.nombre} - {self.periodo}"

# Inscripción
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

# Grupo
class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    #asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True, blank=True)
    estudiantes = models.ManyToManyField(Usuario, limit_choices_to={'rol': 'EST'})
    descripcion = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='grupos_creados', limit_choices_to={'rol': 'DOC'})
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.curso.asignatura.nombre if self.curso and self.curso.asignatura else 'Sin curso'}"
        
    def agregar_estudiante(self, estudiante):
        """Agregar estudiante al grupo"""
        import logging
        logger = logging.getLogger(__name__)
        if estudiante.rol != 'EST':
            raise ValueError('Solo se pueden agregar estudiantes')
        from .models import SolicitudAsignatura
        if self.curso and self.curso.asignatura:
            solicitudes = SolicitudAsignatura.objects.filter(
                estudiante=estudiante,
                asignatura=self.curso.asignatura
            )
            solicitudes_info = [{'id': s.id, 'estado': s.estado} for s in solicitudes]
            logger.info(f"[DEPURACIÓN] Solicitudes encontradas para estudiante {estudiante.email} y asignatura {self.curso.asignatura.id}: {solicitudes_info}")
            print(f"[DEPURACIÓN] Solicitudes encontradas para estudiante {estudiante.email} y asignatura {self.curso.asignatura.id}: {solicitudes_info}")
            if not solicitudes.filter(estado='aceptado').exists():
                raise ValueError('El estudiante no tiene una solicitud aceptada para la asignatura de este curso')
        self.estudiantes.add(estudiante)
    
    def remover_estudiante(self, estudiante):
        """Remover estudiante del grupo"""
        self.estudiantes.remove(estudiante)

# Asignación
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
        return f"{self.titulo} - {self.asignatura.nombre}"

class SolicitudAsignatura(models.Model):
    ESTADOS_SOLICITUD = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS_SOLICITUD, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

class EntregaTarea(models.Model):
    tarea = models.ForeignKey(Asignacion, on_delete=models.CASCADE, related_name='entregas')
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='entregas_tareas')
    archivo = models.FileField(upload_to='entregas/')  # o texto si es digital
    fecha_entregada = models.DateTimeField(auto_now_add=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    grupo = models.ForeignKey(Grupo, null=True, blank=True, on_delete=models.CASCADE)
