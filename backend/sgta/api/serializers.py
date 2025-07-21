from rest_framework import serializers
from ..models import Usuario, Asignatura, PeriodoLectivo, Inscripcion, Asignacion, Grupo

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class AsignaturaSerializer(serializers.ModelSerializer):
    docente_responsable_nombre = serializers.CharField(source='docente_responsable.nombre', read_only=True)
    docente_responsable_apellido = serializers.CharField(source='docente_responsable.apellido', read_only=True)
    
    class Meta:
        model = Asignatura
        fields = '__all__'

class AsignarDocenteSerializer(serializers.Serializer):
    asignatura_id = serializers.IntegerField()
    docente_id = serializers.IntegerField()

class PeriodoLectivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodoLectivo
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AsignacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignacion
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'

class CrearGrupoAleatorioSerializer(serializers.Serializer):
    cantidad_grupos = serializers.IntegerField(min_value=1)
    estudiantes_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

class AsignarTareaSerializer(serializers.Serializer):
    tarea_id = serializers.IntegerField()
    estudiantes_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
    grupos_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'