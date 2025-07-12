from datetime import datetime
from typing import List

class Grupo:
    def __init__(self, id: int, nombre: str, descripcion: str = ""):
        # Campos básicos del grupo
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = datetime.now()
        self.estudiantes_ids: List[int] = []
        self.activo = True
    
    def agregar_estudiante(self, estudiante_id: int) -> bool:
        # Agrega un estudiante al grupo
        if estudiante_id not in self.estudiantes_ids:
            self.estudiantes_ids.append(estudiante_id)
            return True
        return False
    
    def remover_estudiante(self, estudiante_id: int) -> bool:
        # Remueve un estudiante del grupo
        if estudiante_id in self.estudiantes_ids:
            self.estudiantes_ids.remove(estudiante_id)
            return True
        return False
    
    def tiene_estudiante(self, estudiante_id: int) -> bool:
        # Verifica si el estudiante está en el grupo
        return estudiante_id in self.estudiantes_ids
    
    def cantidad_estudiantes(self) -> int:
        # Total de estudiantes en el grupo
        return len(self.estudiantes_ids)
    
    def esta_vacio(self) -> bool:
        # Verifica si el grupo está vacío
        return len(self.estudiantes_ids) == 0
    
    def desactivar(self) -> bool:
        # Desactiva el grupo
        self.activo = False
        return True
    
    def activar(self) -> bool:
        # Activa el grupo
        self.activo = True
        return True
    
    def obtener_estudiantes_ids(self) -> List[int]:
        # Retorna lista de IDs de estudiantes
        return self.estudiantes_ids.copy()
    
    def __str__(self):
        return f"Grupo {self.nombre} ({self.cantidad_estudiantes()} estudiantes)"
