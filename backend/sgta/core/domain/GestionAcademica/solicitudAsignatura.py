from django.db import models
from ..Autenticacion.usuario import Usuario
from ..GestionAcademica.asignatura import Asignatura
from ..GestionAcademica.inscripcion import Inscripcion
from ..GestionTarea.asignacion import Asignacion
from ..GestionTarea.grupo import Grupo

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