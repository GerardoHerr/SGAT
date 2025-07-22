from rest_framework import serializers
from ..models import Usuario, Asignatura, PeriodoLectivo, Inscripcion, Asignacion, Grupo

class UsuarioSerializer(serializers.ModelSerializer):
    contrasenia = serializers.CharField(write_only=True)  # Solo para escritura, no se devuelve en las respuestas
    
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'contrasenia': {'write_only': True}
        }

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
    email = serializers.CharField()
    contrasenia = serializers.CharField()

class AsignacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignacion
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
    estudiantes = UsuarioSerializer(many=True, read_only=True)
    cantidad_estudiantes = serializers.SerializerMethodField()
    asignatura_nombre = serializers.CharField(source='asignatura.nombre', read_only=True)
    
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'asignatura', 'asignatura_nombre', 'estudiantes', 'cantidad_estudiantes', 'descripcion', 'fecha_creacion', 'activo']
    
    def get_cantidad_estudiantes(self, obj):
        return obj.estudiantes.count()

class CrearGrupoAleatorioSerializer(serializers.Serializer):
    asignatura_id = serializers.IntegerField()
    cantidad_grupos = serializers.IntegerField(min_value=1, max_value=20)
    nombre_base = serializers.CharField(max_length=50, default='Grupo')

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