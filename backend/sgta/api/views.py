from rest_framework import viewsets
from ..models import Usuario, Asignatura, PeriodoLectivo, Inscripcion, Asignacion, Grupo
from .serializers import UsuarioSerializer, AsignaturaSerializer,PeriodoLectivoSerializer, LoginSerializer, AsignacionSerializer, GrupoSerializer, CrearGrupoAleatorioSerializer, AsignarTareaSerializer, InscripcionSerializer, InscripcionSerializer, AsignarDocenteSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import random
from django.db import transaction

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_queryset(self):
        queryset = Usuario.objects.all()
        rol = self.request.query_params.get('rol')
        asignatura_id = self.request.query_params.get('asignatura')
        
        if rol:
            queryset = queryset.filter(rol=rol)
        
        if asignatura_id and rol == 'EST':
            # Filtrar estudiantes inscritos en la asignatura específica
            queryset = queryset.filter(
                inscripciones_estudiante__asignatura__id=asignatura_id,
                inscripciones_estudiante__activa=True
            )
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['contrasenia'] = make_password(data['contrasenia'])  # 🔒 Hashear aquí

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'mensaje': 'Usuario registrado con éxito'}, status=status.HTTP_201_CREATED)

class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = Asignatura.objects.all()
    serializer_class = AsignaturaSerializer

    def get_queryset(self):
        """Filtrar asignaturas según el rol del usuario"""
        queryset = Asignatura.objects.all()
        
        # Filtrar por docente si se especifica
        docente_email = self.request.query_params.get('docente_email', None)
        if docente_email:
            try:
                docente = Usuario.objects.get(email=docente_email, rol='DOC')
                queryset = queryset.filter(docente_responsable=docente)
            except Usuario.DoesNotExist:
                queryset = Asignatura.objects.none()
        
        return queryset

    @action(detail=False, methods=['get'])
    def mis_asignaturas(self, request):
        """Obtener asignaturas del docente autenticado"""
        docente_email = request.query_params.get('email')
        if not docente_email:
            return Response(
                {'error': 'Se requiere el email del docente'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            docente = Usuario.objects.get(email=docente_email, rol='DOC')
            asignaturas = Asignatura.objects.filter(docente_responsable=docente)
            serializer = AsignaturaSerializer(asignaturas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Docente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def asignar_docente(self, request):
        """Asignar un docente responsable a una asignatura"""
        try:
            asignatura_id = request.data.get('asignatura_id')
            docente_id = request.data.get('docente_id')  # Este sera el email del docente
            
            if not asignatura_id or not docente_id:
                return Response(
                    {'error': 'Se requieren asignatura_id y docente_id'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            asignatura = Asignatura.objects.get(id=asignatura_id)
            docente = Usuario.objects.get(email=docente_id, rol='DOC')  # Buscar por email
            
            asignatura.docente_responsable = docente
            asignatura.save()
            
            return Response({
                'mensaje': f'Docente {docente.nombre} {docente.apellido} asignado a {asignatura.nombre}',
                'asignatura': AsignaturaSerializer(asignatura).data
            }, status=status.HTTP_200_OK)
            
        except Asignatura.DoesNotExist:
            return Response({'error': 'Asignatura no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Usuario.DoesNotExist:
            return Response({'error': 'Docente no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def docentes_disponibles(self, request):
        """Obtener lista de docentes disponibles para asignar"""
        docentes = Usuario.objects.filter(rol='DOC')
        return Response([{
            'id': docente.email,  # Usar email como ID ya que es la primary key
            'email': docente.email,
            'nombre': docente.nombre,
            'apellido': docente.apellido
        } for docente in docentes], status=status.HTTP_200_OK)

class PeriodoLectivoViewSet(viewsets.ModelViewSet):
    queryset = PeriodoLectivo.objects.all()
    serializer_class = PeriodoLectivoSerializer

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    
    def get_queryset(self):
        queryset = Inscripcion.objects.all()
        asignatura_id = self.request.query_params.get('asignatura_id')
        estudiante_id = self.request.query_params.get('estudiante_id')
        
        if asignatura_id:
            queryset = queryset.filter(asignatura__id=asignatura_id)
        if estudiante_id:
            queryset = queryset.filter(estudiante__id=estudiante_id)
            
        return queryset.filter(activa=True).order_by('-fecha_inscripcion')

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    
    def get_queryset(self):
        queryset = Inscripcion.objects.all()
        estudiante_id = self.request.query_params.get('estudiante_id')
        asignatura_id = self.request.query_params.get('asignatura_id')
        
        if estudiante_id:
            queryset = queryset.filter(estudiante__id=estudiante_id)
        if asignatura_id:
            queryset = queryset.filter(asignatura__id=asignatura_id)
            
        return queryset.filter(activa=True)

class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    
    def get_queryset(self):
        queryset = Asignacion.objects.all()
        docente_id = self.request.query_params.get('docente_id')
        docente_email = self.request.query_params.get('docente_email')
        asignatura_id = self.request.query_params.get('asignatura_id')
        tipo_tarea = self.request.query_params.get('tipo_tarea')
        
        if docente_id:
            queryset = queryset.filter(docente__id=docente_id)
        if docente_email:
            try:
                docente = Usuario.objects.get(email=docente_email, rol='DOC')
                queryset = queryset.filter(docente=docente)
            except Usuario.DoesNotExist:
                queryset = Asignacion.objects.none()
        if asignatura_id:
            queryset = queryset.filter(asignatura__id=asignatura_id)
        if tipo_tarea:
            queryset = queryset.filter(tipo_tarea=tipo_tarea)
            
        return queryset.order_by('-fecha_creacion')
    
    @action(detail=True, methods=['post'])
    def asignar_estudiantes_grupos(self, request, pk=None):
        asignacion = self.get_object()
        serializer = AsignarTareaSerializer(data=request.data)
        
        if serializer.is_valid():
            estudiantes_ids = serializer.validated_data.get('estudiantes_ids', [])
            grupos_ids = serializer.validated_data.get('grupos_ids', [])
            
            with transaction.atomic():
                # Asignar estudiantes individuales
                if estudiantes_ids:
                    estudiantes = Usuario.objects.filter(id__in=estudiantes_ids, rol='EST')
                    asignacion.estudiantes_asignados.add(*estudiantes)
                
                # Asignar grupos
                if grupos_ids:
                    grupos = Grupo.objects.filter(id__in=grupos_ids)
                    asignacion.grupos_asignados.add(*grupos)
            
            return Response({'mensaje': 'Asignación realizada correctamente'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    
    def get_queryset(self):
        queryset = Grupo.objects.all()
        asignatura_id = self.request.query_params.get('asignatura_id')
        
        if asignatura_id:
            queryset = queryset.filter(asignatura__id=asignatura_id)
            
        return queryset.order_by('nombre')
    
    @action(detail=False, methods=['post'])
    def crear_grupos_aleatorios(self, request):
        serializer = CrearGrupoAleatorioSerializer(data=request.data)
        
        if serializer.is_valid():
            asignatura_id = serializer.validated_data['asignatura_id']
            cantidad_grupos = serializer.validated_data['cantidad_grupos']
            nombre_base = serializer.validated_data['nombre_base']
            
            try:
                asignatura = Asignatura.objects.get(id=asignatura_id)
                
                # Obtener estudiantes inscritos en la asignatura
                estudiantes = Usuario.objects.filter(
                    rol='EST',
                    inscripciones_estudiante__asignatura=asignatura,
                    inscripciones_estudiante__activa=True
                )
                
                if estudiantes.count() == 0:
                    return Response(
                        {'error': 'No hay estudiantes inscritos en esta asignatura'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Mezclar estudiantes aleatoriamente
                estudiantes_list = list(estudiantes)
                random.shuffle(estudiantes_list)
                
                # Calcular estudiantes por grupo
                total_estudiantes = len(estudiantes_list)
                estudiantes_por_grupo = total_estudiantes // cantidad_grupos
                estudiantes_sobrantes = total_estudiantes % cantidad_grupos
                
                grupos_creados = []
                
                with transaction.atomic():
                    inicio = 0
                    for i in range(cantidad_grupos):
                        # Calcular el tamaño del grupo actual
                        tamaño_grupo = estudiantes_por_grupo
                        if i < estudiantes_sobrantes:
                            tamaño_grupo += 1
                        
                        # Crear el grupo
                        grupo = Grupo.objects.create(
                            nombre=f"{nombre_base} {i + 1}",
                            asignatura=asignatura,
                            descripcion=f"Grupo creado automáticamente para {asignatura.nombre}"
                        )
                        
                        # Asignar estudiantes al grupo
                        estudiantes_grupo = estudiantes_list[inicio:inicio + tamaño_grupo]
                        grupo.estudiantes.add(*estudiantes_grupo)
                        
                        grupos_creados.append(grupo)
                        inicio += tamaño_grupo
                
                # Serializar los grupos creados
                grupos_serializer = GrupoSerializer(grupos_creados, many=True)
                
                return Response({
                    'mensaje': f'Se crearon {cantidad_grupos} grupos correctamente',
                    'grupos': grupos_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except Asignatura.DoesNotExist:
                return Response(
                    {'error': 'La asignatura no existe'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def agregar_estudiante(self, request, pk=None):
        grupo = self.get_object()
        estudiante_id = request.data.get('estudiante_id')
        
        try:
            estudiante = Usuario.objects.get(id=estudiante_id, rol='EST')
            grupo.agregar_estudiante(estudiante)
            return Response({'mensaje': 'Estudiante agregado al grupo'}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def remover_estudiante(self, request, pk=None):
        grupo = self.get_object()
        estudiante_id = request.data.get('estudiante_id')
        
        try:
            estudiante = Usuario.objects.get(id=estudiante_id, rol='EST')
            grupo.remover_estudiante(estudiante)
            return Response({'mensaje': 'Estudiante removido del grupo'}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            contrasenia = serializer.validated_data['contrasenia']

            try:
                user = Usuario.objects.get(email=email)
                # Verificar contraseña (comparación directa ya que están en texto plano)
                if contrasenia == user.contrasenia:
                    payload = {
                        'id': user.email,
                        'email': user.email,
                        'rol': user.rol,
                        'exp': datetime.utcnow() + timedelta(minutes=30),
                        'iat': datetime.utcnow(),
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    return Response({'access': token})
                return Response({'error': 'Credenciales invalidas'}, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)