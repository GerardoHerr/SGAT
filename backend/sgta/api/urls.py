from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sgta.api.views import UsuarioViewSet
from sgta.api.views import AsignaturaViewSet
from rest_framework_simplejwt.views import TokenObtainPairView


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'asignaturas', AsignaturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]


