from rest_framework import serializers
from sgta.core.domain.Autenticacion import Usuario
from sgta.core.domain.GestionTarea import Asignacion, Grupo
from sgta.core.domain.GestionAcademica import Asignatura, PeriodoLectivo, Inscripcion, SolicitudAsignatura, EntregaTarea
from sgta.core.domain.GestionAcademica.curso import Curso

class UsuarioSerializer(serializers.ModelSerializer):
    contrasenia = serializers.CharField(write_only=True)  # Solo para escritura, no se devuelve en las respuestas
    
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.email

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
    curso = serializers.PrimaryKeyRelatedField(read_only=True)
    curso_nombre = serializers.CharField(source='curso.asignatura.nombre', read_only=True)

    class Meta:
        model = Grupo
        fields = [
            'id', 'nombre', 'curso', 'curso_nombre',
            'estudiantes', 'cantidad_estudiantes',
            'descripcion', 'fecha_creacion', 'activo'
        ]

    def get_cantidad_estudiantes(self, obj):
        return obj.estudiantes.count()

class CrearGrupoAleatorioSerializer(serializers.Serializer):
    asignatura_id = serializers.IntegerField()
    cantidad_grupos = serializers.IntegerField(min_value=1, max_value=20)
    nombre_base = serializers.CharField(max_length=50, default='Grupo')

class AsignarTareaSerializer(serializers.Serializer):
    tarea_id = serializers.IntegerField()
    estudiantes_ids = serializers.ListField(
        child=serializers.CharField(),  # emails como IDs
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

class SolicitudAsignaturaSerializer(serializers.ModelSerializer):
    estudiante = serializers.SerializerMethodField()
    asignatura = serializers.SerializerMethodField()

    class Meta:
        model = SolicitudAsignatura
        fields = ['id', 'estado', 'fecha_solicitud', 'estudiante', 'asignatura']

    def get_estudiante(self, obj):
        return obj.estudiante.__str__()

    def get_asignatura(self, obj):
        return obj.asignatura.__str__()  # asegúrate de que el modelo Asignatura tenga un campo 'nombre'
    
class CursoSerializer(serializers.ModelSerializer):
    asignatura_nombre = serializers.CharField(source='asignatura.nombre', read_only=True)
    docente_nombre = serializers.SerializerMethodField()
    cantidad_estudiantes = serializers.SerializerMethodField()
    
    class Meta:
        model = Curso
        fields = ['id', 'asignatura', 'asignatura_nombre', 'docente', 'docente_nombre', 'periodo', 'cantidad_estudiantes']
        # Excluimos el campo 'estudiantes' para evitar cargar todos los estudiantes automáticamente
    
    def get_docente_nombre(self, obj):
        if obj.docente:
            return f"{obj.docente.nombre} {obj.docente.apellido}"
        return "Sin asignar"
    
    def get_cantidad_estudiantes(self, obj):
        return obj.estudiantes.count()

# Serializer para EntregaTarea
class EntregaTareaSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.nombre', read_only=True)
    estudiante_email = serializers.CharField(source='estudiante.email', read_only=True)
    grupo_nombre = serializers.CharField(source='grupo.nombre', read_only=True, default=None)
    tarea_titulo = serializers.CharField(source='tarea.titulo', read_only=True)

    class Meta:
        model = EntregaTarea
        fields = '__all__'
        # Puedes personalizar los campos si lo deseas