from rest_framework import serializers
from sgta.models import Usuario
from sgta.models import Asignatura

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class AsignaturaSerializer(serializers.ModelSerializer):
    #registrada_por = UsuarioSerializer(read_only=True)

    class Meta:
        model = Asignatura
        fields = '__all__'
        #read_only_fields = ('fecha_creacion', 'registrada_por')    