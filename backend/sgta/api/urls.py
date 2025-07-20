from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sgta.api.views import UsuarioViewSet,PeriodoLectivoViewSet  
from sgta.api.views import LoginView
from sgta.api.views import AsignaturaViewSet


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'periodos', PeriodoLectivoViewSet)  
router.register(r'asignaturas', AsignaturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]


