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
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)

