from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from sgta.api.views import UsuarioViewSet,PeriodoLectivoViewSet, AsignacionViewSet, GrupoViewSet, InscripcionViewSet, EntregaTareaViewSet  
from sgta.api.views import LoginView
from sgta.api.views import AsignaturaViewSet
from sgta.api.views import SolicitarAsignaturaViewSet

from sgta.api.views import CursoViewSet

from sgta.api.views import ReporteTareasCursoPDFView


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'periodos', PeriodoLectivoViewSet)  
router.register(r'asignaturas', AsignaturaViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'asignaciones', AsignacionViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'solicitudAsignatura', SolicitarAsignaturaViewSet)

router.register(r'entregas', EntregaTareaViewSet, basename='entregatarea')




urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('reportes/curso/pdf/', ReporteTareasCursoPDFView.as_view(), name='reporte-tareas-curso-pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


