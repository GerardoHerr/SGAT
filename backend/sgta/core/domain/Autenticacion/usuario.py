from django.db import models

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