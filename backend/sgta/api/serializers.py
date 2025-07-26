from rest_framework import serializers

# Importar modelos desde el dominio
from ..core.domain.Autenticacion.usuario import Usuario
from ..core.domain.GestionAcademica.asignatura import Asignatura
from ..core.domain.GestionAcademica.periodo_lectivo import PeriodoLectivo
from ..core.domain.GestionAcademica.inscripcion import Inscripcion
from ..core.domain.GestionTarea.asignacion import Asignacion
from ..core.domain.GestionTarea.grupo import Grupo
from ..core.domain.GestionTarea.calificacion import Calificacion
from ..core.domain.GestionAcademica.solicitudAsignatura import SolicitudAsignatura

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

class SolicitudAsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudAsignatura
        fields = '__all__'

class CalificacionSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.nombre', read_only=True)
    estudiante_apellido = serializers.CharField(source='estudiante.apellido', read_only=True)
    tarea_titulo = serializers.CharField(source='tarea.titulo', read_only=True)
    tipo_tarea = serializers.CharField(source='tarea.tipo_tarea', read_only=True)
    calificado_por_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Calificacion
        fields = [
            'id', 'tarea', 'tarea_titulo', 'tipo_tarea', 'estudiante', 
            'estudiante_nombre', 'estudiante_apellido', 'calificacion', 
            'retroalimentacion', 'fecha_calificacion', 'calificado_por',
            'calificado_por_nombre'
        ]
        read_only_fields = ['fecha_calificacion', 'calificado_por']
    
    def get_calificado_por_nombre(self, obj):
        if obj.calificado_por:
            return f"{obj.calificado_por.nombre} {obj.calificado_por.apellido}"
        return None
    
    def validate(self, data):
        # Validar que el usuario que califica sea docente
        user = self.context['request'].user
        if not user or user.rol != 'DOC':
            raise serializers.ValidationError("Solo los docentes pueden calificar tareas.")
        
        # Validar que la calificación esté dentro del rango permitido según el tipo de tarea
        tarea = data.get('tarea') or self.instance and self.instance.tarea
        calificacion = data.get('calificacion')
        
        if calificacion is not None and tarea:
            if tarea.tipo_tarea == 'ACD' and (calificacion < 0 or calificacion > 1.0):
                raise serializers.ValidationError("La calificación para ACD debe estar entre 0 y 1.0")
            elif tarea.tipo_tarea == 'AA' and (calificacion < 0 or calificacion > 1.5):
                raise serializers.ValidationError("La calificación para AA debe estar entre 0 y 1.5")
            elif tarea.tipo_tarea == 'APE' and (calificacion < 0 or calificacion > 2.5):
                raise serializers.ValidationError("La calificación para APE debe estar entre 0 y 2.5")
        
        return data
    
    def create(self, validated_data):
        # Asignar automáticamente el usuario que está calificando
        validated_data['calificado_por'] = self.context['request'].user
        return super().create(validated_data)

class CalificacionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ['calificacion', 'retroalimentacion']
    
    def update(self, instance, validated_data):
        # Actualizar solo los campos permitidos
        instance.calificacion = validated_data.get('calificacion', instance.calificacion)
        instance.retroalimentacion = validated_data.get('retroalimentacion', instance.retroalimentacion)
        instance.save()
        return instance