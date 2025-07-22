from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sgta.api.views import UsuarioViewSet,PeriodoLectivoViewSet, AsignacionViewSet, GrupoViewSet, InscripcionViewSet  
from sgta.api.views import LoginView
from sgta.api.views import AsignaturaViewSet


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'periodos', PeriodoLectivoViewSet)  
router.register(r'asignaturas', AsignaturaViewSet)
router.register(r'inscripciones', InscripcionViewSet)
router.register(r'asignaciones', AsignacionViewSet)
router.register(r'grupos', GrupoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]


