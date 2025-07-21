# Exportar todas las clases del módulo GestionAcademica
from .asignatura import Asignatura
from .periodo_lectivo import PeriodoLectivo
from .solicitudAsignatura import SolicitudAsignatura

__all__ = ['Asignatura', 'PeriodoLectivo', 'SolicitudAsignatura']