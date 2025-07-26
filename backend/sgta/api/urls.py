from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sgta.api.views import UsuarioViewSet,PeriodoLectivoViewSet, AsignacionViewSet, GrupoViewSet, InscripcionViewSet, EntregaTareaViewSet  
from sgta.api.views import LoginView
from sgta.api.views import AsignaturaViewSet
from sgta.api.views import SolicitarAsignaturaViewSet  # Asegúrate de tener este ViewSet definido
from sgta.api.views import CursoViewSet  # Asegúrate de tener este ViewSet definido

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'periodos', PeriodoLectivoViewSet)  
router.register(r'asignaturas', AsignaturaViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'asignaciones', AsignacionViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'solicitudAsignatura', SolicitarAsignaturaViewSet, basename='solicitudasignatura')

router.register(r'entregas', EntregaTareaViewSet, basename='entregatarea')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
