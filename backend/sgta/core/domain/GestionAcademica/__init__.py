# Exportar todas las clases del módulo GestionAcademica
from .asignatura import Asignatura
from .periodo_lectivo import PeriodoLectivo
from .inscripcion import Inscripcion
from .solicitudAsignatura import SolicitudAsignatura
from .entregarTarea import EntregaTarea

__all__ = ['Asignatura', 'PeriodoLectivo', 'Inscripcion', 'SolicitudAsignatura', 'EntregaTarea']

