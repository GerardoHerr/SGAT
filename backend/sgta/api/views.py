from rest_framework import viewsets
<<<<<<< HEAD
from ..core.domain import *
from .serializers import UsuarioSerializer, AsignaturaSerializer,PeriodoLectivoSerializer
=======
from sgta.models import Usuario
from sgta.models import Asignatura
from sgta.api.serializers import UsuarioSerializer
from sgta.api.serializers import AsignaturaSerializer
>>>>>>> sergio

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer

<<<<<<< HEAD
class PeriodoLectivoViewSet(viewsets.ModelViewSet):
    queryset = PeriodoLectivo.objects.all()
    serializer_class = PeriodoLectivoSerializer
=======
    def perform_create(self, serializer):
        # Automatically set the user who created the subject
        serializer.save(registrada_por=self.request.user)
>>>>>>> sergio
