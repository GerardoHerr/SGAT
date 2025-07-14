# Exportar todas las clases de todos los módulos del domain
from .Autenticacion import *
from .GestionAcademica import *
from .GestionTarea import *

# Lista de todas las clases disponibles
__all__ = [
    # Autenticacion
    'Usuario',
    # GestionAcademica
    'Asignatura',
    # GestionTarea
    'Asignacion',
    'Grupo',
]