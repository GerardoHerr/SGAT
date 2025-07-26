from django.db import models
from datetime import date
from ..Autenticacion.usuario import Usuario
from .grupo import Grupo

class Asignacion(models.Model):
    TIPO_TAREA_CHOICES = [
        ('ACD', 'Aprendizaje en Contacto con el Docente'),
        ('AA', 'Aprendizaje Autónomo'),
        ('APE', 'Aprendizaje Práctico Experimental'),
    ]
    
    # Campos básicos
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()
    tipo_tarea = models.CharField(max_length=3, choices=TIPO_TAREA_CHOICES)
    es_grupal = models.BooleanField(default=False)
    docente = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_asignadas')
    
    # Campos opcionales
    rubrica = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    activa = models.BooleanField(default=True)
    
    # Relaciones
    estudiantes_asignados = models.ManyToManyField(Usuario, related_name='tareas_recibidas', blank=True)
    grupos_asignados = models.ManyToManyField(Grupo, related_name='tareas_grupales', blank=True)
    
    class Meta:
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'
        ordering = ['-fecha_creacion']
    
    def establecer_rubrica(self, rubrica: str) -> bool:
        # Agrega rúbrica si es válida
        if rubrica and len(rubrica.strip()) > 0:
            self.rubrica = rubrica
            self.save()
            return True
        return False
    
    def asignar_a_estudiante(self, estudiante: Usuario) -> bool:
        # Solo para tareas individuales
        if self.es_grupal:
            return False
        
        if not self.estudiantes_asignados.filter(id=estudiante.id).exists():
            self.estudiantes_asignados.add(estudiante)
            return True
        return False
    
    def asignar_a_estudiantes(self, estudiantes) -> bool:
        # Asigna múltiples estudiantes (individual)
        if self.es_grupal:
            return False
        
        for estudiante in estudiantes:
            if not self.estudiantes_asignados.filter(id=estudiante.id).exists():
                self.estudiantes_asignados.add(estudiante)
        return True
    
    def asignar_a_grupo(self, grupo) -> bool:
        # Solo para tareas grupales
        if not self.es_grupal:
            return False
        
        if not self.grupos_asignados.filter(id=grupo.id).exists():
            self.grupos_asignados.add(grupo)
            # Agregar estudiantes del grupo a lista general
            for estudiante in grupo.estudiantes.all():
                if not self.estudiantes_asignados.filter(id=estudiante.id).exists():
                    self.estudiantes_asignados.add(estudiante)
            return True
        return False
    
    def asignar_a_grupos(self, grupos) -> bool:
        # Asigna múltiples grupos
        if not self.es_grupal:
            return False
        
        for grupo in grupos:
            self.asignar_a_grupo(grupo)
        return True
    
    def es_tipo_valido(self) -> bool:
        # Valida tipo ACD, AA, APE
        tipos_validos = ['ACD', 'AA', 'APE']
        return self.tipo_tarea in tipos_validos
    
    def obtener_puntos_tipo(self) -> float:
        # Puntos según tipo de tarea
        puntos_map = {
            'ACD': 2.0,  # Aprendizaje en Contacto con el Docente
            'AA': 2.0,   # Aprendizaje Autónomo
            'APE': 2.5   # Aprendizaje Práctico Experimental
        }
        return puntos_map.get(self.tipo_tarea, 0.0)
    
    def tiene_rubrica(self) -> bool:
        # Verifica si tiene rúbrica
        return self.rubrica is not None and len(self.rubrica.strip()) > 0
    
    def esta_vencida(self) -> bool:
        # Verifica si ya venció
        return date.today() > self.fecha_entrega
    
    def puede_ser_visualizada_por_estudiante(self, estudiante: Usuario) -> bool:
        # Verifica si estudiante puede ver la tarea
        return self.activa and self.estudiantes_asignados.filter(id=estudiante.id).exists()
    
    def obtener_grupo_de_estudiante(self, estudiante: Usuario):
        # Obtiene grupo del estudiante (si es grupal)
        if not self.es_grupal:
            return None
        
        for grupo in self.grupos_asignados.all():
            if grupo.estudiantes.filter(id=estudiante.id).exists():
                return grupo
        return None
    
    def cantidad_estudiantes_asignados(self) -> int:
        # Total de estudiantes asignados
        return self.estudiantes_asignados.count()
    
    def cantidad_grupos(self) -> int:
        # Total de grupos (si es grupal)
        return self.grupos_asignados.count() if self.es_grupal else 0
    
    def desactivar(self) -> bool:
        # Desactiva la asignación
        self.activa = False
        self.save()
        return True
    
    def activar(self) -> bool:
        # Activa la asignación
        self.activa = True
        self.save()
        return True
    
    def validar_campos_obligatorios(self) -> bool:
        # Valida campos requeridos
        campos_validos = (
            self.titulo and len(self.titulo.strip()) > 0 and
            self.descripcion and len(self.descripcion.strip()) > 0 and
            self.fecha_entrega is not None and
            self.es_tipo_valido() and
            self.docente_id is not None
        )
        return campos_validos
    
    def obtener_resumen(self) -> dict:
        # Resumen para visualización
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'tipo_tarea': self.tipo_tarea,
            'puntos': self.obtener_puntos_tipo(),
            'es_grupal': self.es_grupal,
            'fecha_entrega': self.fecha_entrega.strftime('%Y-%m-%d'),
            'tiene_rubrica': self.tiene_rubrica(),
            'cantidad_estudiantes': self.cantidad_estudiantes_asignados(),
            'cantidad_grupos': self.cantidad_grupos(),
            'esta_vencida': self.esta_vencida(),
            'activa': self.activa
        }
    
    def __str__(self):
        tipo_asignacion = "Grupal" if self.es_grupal else "Individual"
        return f"{self.titulo} ({self.tipo_tarea} - {tipo_asignacion})"
