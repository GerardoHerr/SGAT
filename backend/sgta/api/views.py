from rest_framework import viewsets
from sgta.models import Usuario
from sgta.api.serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer