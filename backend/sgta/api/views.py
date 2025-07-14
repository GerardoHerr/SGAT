from rest_framework import viewsets
from sgta.models import Usuario
from sgta.models import Asignatura
from sgta.api.serializers import UsuarioSerializer
from sgta.api.serializers import AsignaturaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer

    def perform_create(self, serializer):
        # Automatically set the user who created the subject
        serializer.save(registrada_por=self.request.user)