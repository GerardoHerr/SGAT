from datetime import datetime, date
from typing import List, Optional
from .grupo import Grupo

class Asignacion:
    def __init__(self, id: int, titulo: str, descripcion: str, fecha_entrega: date,
                 tipo_tarea: str, es_grupal: bool, docente_id: int):
        # Campos básicos
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_entrega = fecha_entrega
        self.tipo_tarea = tipo_tarea  # 'ACD', 'AA', 'APE'
        self.es_grupal = es_grupal
        self.docente_id = docente_id
        
        # Campos opcionales
        self.rubrica = None
        self.fecha_creacion = datetime.now()
        self.estudiantes_asignados: List[int] = []
        self.grupos_asignados: List[Grupo] = []
        self.activa = True
    
    def establecer_rubrica(self, rubrica: str) -> bool:
        # Agrega rúbrica si es válida
        if rubrica and len(rubrica.strip()) > 0:
            self.rubrica = rubrica
            return True
        return False
    
    def asignar_a_estudiante(self, estudiante_id: int) -> bool:
        # Solo para tareas individuales
        if self.es_grupal:
            return False
        
        if estudiante_id not in self.estudiantes_asignados:
            self.estudiantes_asignados.append(estudiante_id)
            return True
        return False
    
    def asignar_a_estudiantes(self, estudiantes_ids: List[int]) -> bool:
        # Asigna múltiples estudiantes (individual)
        if self.es_grupal:
            return False
        
        for estudiante_id in estudiantes_ids:
            if estudiante_id not in self.estudiantes_asignados:
                self.estudiantes_asignados.append(estudiante_id)
        return True
    
    def asignar_a_grupo(self, grupo: Grupo) -> bool:
        # Solo para tareas grupales
        if not self.es_grupal:
            return False
        
        if grupo not in self.grupos_asignados:
            self.grupos_asignados.append(grupo)
            # Agregar estudiantes del grupo a lista general
            for estudiante_id in grupo.obtener_estudiantes_ids():
                if estudiante_id not in self.estudiantes_asignados:
                    self.estudiantes_asignados.append(estudiante_id)
            return True
        return False
    
    def asignar_a_grupos(self, grupos: List[Grupo]) -> bool:
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
    
    def puede_ser_visualizada_por_estudiante(self, estudiante_id: int) -> bool:
        # Verifica si estudiante puede ver la tarea
        return self.activa and estudiante_id in self.estudiantes_asignados
    
    def obtener_grupo_de_estudiante(self, estudiante_id: int) -> Optional[Grupo]:
        # Obtiene grupo del estudiante (si es grupal)
        if not self.es_grupal:
            return None
        
        for grupo in self.grupos_asignados:
            if grupo.tiene_estudiante(estudiante_id):
                return grupo
        return None
    
    def cantidad_estudiantes_asignados(self) -> int:
        # Total de estudiantes asignados
        return len(self.estudiantes_asignados)
    
    def cantidad_grupos(self) -> int:
        # Total de grupos (si es grupal)
        return len(self.grupos_asignados) if self.es_grupal else 0
    
    def desactivar(self) -> bool:
        # Desactiva la asignación
        self.activa = False
        return True
    
    def activar(self) -> bool:
        # Activa la asignación
        self.activa = True
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
