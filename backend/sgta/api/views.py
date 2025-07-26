from datetime import datetime, timedelta
import jwt
import random

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

# Importar modelos desde el dominio
from ..core.domain.Autenticacion.usuario import Usuario
from ..core.domain.GestionAcademica.asignatura import Asignatura
from ..core.domain.GestionAcademica.periodo_lectivo import PeriodoLectivo
from ..core.domain.GestionAcademica.inscripcion import Inscripcion
from ..core.domain.GestionTarea.asignacion import Asignacion
from ..core.domain.GestionTarea.grupo import Grupo
from ..core.domain.GestionAcademica.solicitudAsignatura import SolicitudAsignatura
from ..core.domain.GestionTarea.calificacion import Calificacion

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import BasicAuthentication

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import (
    UsuarioSerializer, AsignaturaSerializer, 
    PeriodoLectivoSerializer, LoginSerializer, 
    AsignacionSerializer, GrupoSerializer, 
    CrearGrupoAleatorioSerializer, AsignarTareaSerializer, 
    InscripcionSerializer, AsignarDocenteSerializer,
    CalificacionSerializer, CalificacionUpdateSerializer
)

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
    
    @action(detail=False, methods=['get'], url_path='by-email')
    def get_by_email(self, request):
        """Obtener usuario por email - usado después del login"""
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email requerido'}, status=400)
        
        try:
            usuario = Usuario.objects.get(email=email)
            serializer = self.get_serializer(usuario)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)
    
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

class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación
    
    def post(self, request, *args, **kwargs):
        # Obtener datos del body de la petición
        print("\n=== NUEVA SOLICITUD DE AUTENTICACIÓN ===")
        print("Headers:", request.headers)
        print("Content-Type:", request.content_type)
        print("Método:", request.method)
        
        try:
            data = request.data
            print("Datos recibidos (raw):", data)
            
            # Verificar si los datos son un QueryDict (como en form-data)
            if hasattr(data, 'getlist'):
                print("Los datos están en formato form-data")
                email = data.get('email', [''])[0].strip()
                password = data.get('password', [''])[0].strip()
            else:
                print("Los datos están en formato JSON")
                email = data.get('email', '').strip()
                password = data.get('password', '').strip()
            
            print(f"Email extraído: '{email}'")
            print(f"Contraseña recibida: {'*' * len(password) if password else 'vacía'}")
            
            if not email or not password:
                return Response(
                    {'error': 'Se requieren email y contraseña'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            print(f"Buscando usuario con email: '{email}'")
            try:
                user = Usuario.objects.get(email=email)
                print(f"Usuario encontrado: {user.email}")
                
                # Verificar contraseña (compatibilidad con texto plano y hash)
                print(f"Contraseña almacenada: {user.contrasenia[:10]}...")
                
                # Si la contraseña almacenada no parece ser un hash, comparar directamente
                if len(user.contrasenia) < 30:  # Los hashes son más largos
                    is_valid = (password == user.contrasenia)
                    # Si la contraseña es correcta, actualizarla a hash
                    if is_valid:
                        user.contrasenia = make_password(password)
                        user.save()
                        print("Contraseña actualizada a hash seguro")
                else:
                    # Verificar contraseña hasheada
                    is_valid = check_password(password, user.contrasenia)
                
                print(f"¿Contraseña válida? {is_valid}")
                
                if not is_valid:
                    # Para depuración: mostrar los primeros 3 caracteres de la contraseña proporcionada
                    print(f"Contraseña proporcionada (primeros 3 caracteres): {password[:3]}{'*' * (len(password) - 3) if len(password) > 3 else ''}")
                    return Response(
                        {'error': 'Credenciales inválidas'}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                    
                # Generar tokens
                print("Generando tokens JWT...")
                refresh = RefreshToken.for_user(user)
                print("Tokens generados exitosamente")
            
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'email': user.email,
                        'nombre': user.nombre,
                        'apellido': user.apellido,
                        'rol': user.rol
                    }
                }, status=status.HTTP_200_OK)
                
            except Usuario.DoesNotExist:
                print("Usuario no encontrado")  # Depuración
                return Response(
                    {'error': 'Credenciales inválidas'},  # No revelar que el usuario no existe
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
        except Exception as e:
            # Obtener información detallada del error
            import traceback
            error_traceback = traceback.format_exc()
            error_message = str(e)
            
            print("\n=== ERROR DETALLADO ===")
            print(f"Tipo de error: {type(e).__name__}")
            print(f"Mensaje de error: {error_message}")
            print("Traceback completo:")
            print(error_traceback)
            print("======================\n")
            
            # Devolver el error real en desarrollo (solo para depuración)
            import sys
            return Response(
                {
                    'error': 'Error en el servidor al procesar la autenticación',
                    'detail': error_message,
                    'type': type(e).__name__,
                    'traceback': error_traceback if settings.DEBUG else None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    def post(self, request):
        # Crear una instancia de la vista de token JWT
        view = CustomTokenObtainPairView.as_view()
        # Llamar a la vista con el request original
        return view(request._request if hasattr(request, '_request') else request)

class CalificacionViewSet(viewsets.ModelViewSet):
    """
    API para gestionar calificaciones de tareas
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Calificacion.objects.all()
        
        # Filtrar por tarea si se proporciona el parámetro
        tarea_id = self.request.query_params.get('tarea_id')
        if tarea_id:
            queryset = queryset.filter(tarea_id=tarea_id)
        
        # Filtrar por estudiante si se proporciona el parámetro
        estudiante_id = self.request.query_params.get('estudiante_id')
        if estudiante_id:
            queryset = queryset.filter(estudiante_id=estudiante_id)
        
        # Si es un docente, solo puede ver las calificaciones de sus asignaturas
        if user.rol == 'DOC':
            queryset = queryset.filter(tarea__asignatura__docente_responsable=user)
        # Si es un estudiante, solo puede ver sus propias calificaciones
        elif user.rol == 'EST':
            queryset = queryset.filter(estudiante=user)
            
        return queryset.select_related('tarea', 'estudiante', 'calificado_por')
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CalificacionUpdateSerializer
        return CalificacionSerializer
    
    def perform_create(self, serializer):
        # Asignar automáticamente el usuario que está calificando
        serializer.save(calificado_por=self.request.user)
    
    @action(detail=False, methods=['get'], url_path=r'por-tarea/(?P<tarea_id>\d+)')
    def por_tarea(self, request, tarea_id=None):
        """
        Obtener todas las calificaciones de una tarea específica
        """
        # Verificar que la tarea existe
        tarea = get_object_or_404(Asignacion, id=tarea_id)
        
        # Verificar permisos
        if request.user.rol == 'DOC' and tarea.creada_por != request.user:
            return Response(
                {"error": "No tiene permiso para ver las calificaciones de esta tarea"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        calificaciones = self.get_queryset().filter(tarea=tarea)
        serializer = self.get_serializer(calificaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path=r'estudiantes-sin-calificar/(?P<tarea_id>\d+)')
    def estudiantes_sin_calificar(self, request, tarea_id=None):
        """
        Obtener lista de estudiantes que no han sido calificados para una tarea
        """
        tarea = get_object_or_404(Asignacion, id=tarea_id)
        
        # Verificar permisos
        if request.user.rol != 'DOC' or tarea.creada_por != request.user:
            return Response(
                {"error": "No tiene permiso para ver esta información"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener estudiantes asignados a la tarea (individual o por grupo)
        if tarea.es_grupal:
            # Si es grupal, obtener estudiantes de los grupos asignados
            estudiantes_ids = Usuario.objects.filter(
                grupos_estudiante__in=tarea.grupos_asignados.all()
            ).values_list('id', flat=True)
        else:
            # Si es individual, obtener estudiantes asignados directamente
            estudiantes_ids = tarea.estudiantes_asignados.values_list('id', flat=True)
        
        # Filtrar estudiantes que ya tienen calificación para esta tarea
        estudiantes_calificados = Calificacion.objects.filter(
            tarea=tarea,
            estudiante_id__in=estudiantes_ids
        ).values_list('estudiante_id', flat=True)
        
        # Obtener estudiantes sin calificar
        estudiantes_sin_calificar = Usuario.objects.filter(
            id__in=estudiantes_ids
        ).exclude(
            id__in=estudiantes_calificados
        )
        
        # Serializar la información básica de los estudiantes
        estudiantes_data = [
            {
                'id': est.id,
                'nombre': est.nombre,
                'apellido': est.apellido,
                'email': est.email
            }
            for est in estudiantes_sin_calificar
        ]
        
        return Response({
            'tarea_id': tarea.id,
            'tarea_titulo': tarea.titulo,
            'estudiantes_sin_calificar': estudiantes_data,
            'total_estudiantes': len(estudiantes_ids),
            'estudiantes_calificados': len(estudiantes_calificados),
            'estudiantes_sin_calificar_count': len(estudiantes_data)
        })
