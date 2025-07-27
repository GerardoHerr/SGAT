from django.db import models
from ..Autenticacion.usuario import Usuario
from ..GestionAcademica.curso import Curso

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
        from ..GestionAcademica.solicitudAsignatura import SolicitudAsignatura
        """Agregar estudiante al grupo"""
        import logging
        logger = logging.getLogger(__name__)
        if estudiante.rol != 'EST':
            raise ValueError('Solo se pueden agregar estudiantes')
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
