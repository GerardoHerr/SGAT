from django.db import models

class Usuario(models.Model): 
    ROL_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('DOC', 'Docente'),
        ('EST', 'Estudiante'),
    ]

    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    contrasenia = models.CharField(max_length=200)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"