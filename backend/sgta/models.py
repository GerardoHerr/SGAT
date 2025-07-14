from django.db import models

class Usuario(models.Model): 
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('DOC', 'Docente'),
        ('EST', 'Estudiante'),
    ]

    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.EmailField(unique=False)
    contrasenia = models.CharField(max_length=200)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='EST')

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"

# Modelo para Asignaturas
# Representa las asignaturas del sistema, con un código único, nombre, descripción y estado
class Asignatura(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)  # estado
    
    registrada_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        db_table = 'asignaturas'
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'