from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from sgta.api.views import (
    UsuarioViewSet, PeriodoLectivoViewSet, AsignacionViewSet, 
    GrupoViewSet, InscripcionViewSet, LoginView, AsignaturaViewSet,
    CalificacionViewSet, CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'periodos', PeriodoLectivoViewSet)  
router.register(r'asignaturas', AsignaturaViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'asignaciones', AsignacionViewSet)
router.register(r'grupos', GrupoViewSet)
# router.register(r'solicitudAsignatura', SolicitarAsignaturaViewSet, basename='solicitudasignatura')
router.register(r'calificaciones', CalificacionViewSet, basename='calificaciones')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
