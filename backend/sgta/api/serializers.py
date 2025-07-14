from rest_framework import serializers
from ..core.domain.Autenticacion.usuario import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'