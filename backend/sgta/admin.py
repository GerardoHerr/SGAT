from django.contrib import admin
from django.urls import path

# Importar modelos desde el dominio
from .core.domain.Autenticacion.usuario import Usuario
from .core.domain.GestionAcademica.asignatura import Asignatura
from .core.domain.GestionAcademica.periodo_lectivo import PeriodoLectivo
from .core.domain.GestionAcademica.inscripcion import Inscripcion
from .core.domain.GestionTarea.asignacion import Asignacion
from .core.domain.GestionTarea.grupo import Grupo

# Registrar modelos en el admin de Django
admin.site.register(Usuario)
admin.site.register(Asignatura)
admin.site.register(PeriodoLectivo)
admin.site.register(Inscripcion)
admin.site.register(Asignacion)
admin.site.register(Grupo)

urlpatterns = [
    path('admin/', admin.site.urls),
]