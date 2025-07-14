from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sgta.api.views import UsuarioViewSet,PeriodoLectivoViewSet  # Assuming you have these viewsets defined
from rest_framework_simplejwt.views import TokenObtainPairView


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'asignatura', TokenObtainPairView)
router.register(r'periodos', PeriodoLectivoViewSet)  # Assuming you have a PeriodoLectivoViewSet

urlpatterns = [
    path('', include(router.urls)),
    #path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]