from rest_framework import viewsets
from sgta.models import Tarea
from sgta.api.serializers import TareaSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer