from rest_framework import viewsets
from ..models import Usuario, Asignatura, PeriodoLectivo, Inscripcion, Asignacion, Grupo, SolicitudAsignatura, Curso, EntregaTarea
from .serializers import UsuarioSerializer, AsignaturaSerializer,PeriodoLectivoSerializer, LoginSerializer, AsignacionSerializer, GrupoSerializer, CrearGrupoAleatorioSerializer, AsignarTareaSerializer, InscripcionSerializer, InscripcionSerializer, AsignarDocenteSerializer, SolicitudAsignaturaSerializer, CursoSerializer, EntregaTareaSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
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
                SolicitudAsignatura__asignatura__id=asignatura_id,
                SolicitudAsignatura__estado='aceptado'

                #inscripciones_estudiante__asignatura__id=asignatura_id,
                #inscripciones_estudiante__activa=True
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
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # Si viene 'docente' en el request, usarlo para creada_por
        docente_email = data.get('docente')
        if docente_email:
            try:
                docente = Usuario.objects.get(email=docente_email, rol='DOC')
                data['creada_por'] = docente.pk
            except Usuario.DoesNotExist:
                return Response({'error': 'Docente no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    
    def get_queryset(self):
        queryset = Asignacion.objects.all()
        docente_id = self.request.query_params.get('docente_id')
        docente_email = self.request.query_params.get('docente_email')
        curso_id = self.request.query_params.get('curso')
        tipo_tarea = self.request.query_params.get('tipo_tarea')
        tarea_id = self.request.query_params.get('tarea_id')

        if docente_id:
            queryset = queryset.filter(creada_por__id=docente_id)
        if docente_email:
            try:
                docente = Usuario.objects.get(email=docente_email, rol='DOC')
                queryset = queryset.filter(creada_por=docente)
            except Usuario.DoesNotExist:
                queryset = Asignacion.objects.none()
        if curso_id:
            queryset = queryset.filter(curso__id=curso_id)
        if tipo_tarea:
            queryset = queryset.filter(tipo_tarea=tipo_tarea)

        return queryset.order_by('-fecha_creacion')
    
    @action(detail=True, methods=['post'])
    def asignar_estudiantes_grupos(self, request, pk=None):
        import logging
        logger = logging.getLogger(__name__)
        asignacion = self.get_object()
        serializer = AsignarTareaSerializer(data=request.data)
        if serializer.is_valid():
            estudiantes_ids = serializer.validated_data.get('estudiantes_ids', [])
            grupos_ids = serializer.validated_data.get('grupos_ids', [])
            logger.info(f"[DEPURACIÓN] estudiantes_ids recibidos: {estudiantes_ids}")
            logger.info(f"[DEPURACIÓN] grupos_ids recibidos: {grupos_ids}")
            try:
                with transaction.atomic():
                    estudiantes_creados = set()
                    # Asignar estudiantes individuales
                    if estudiantes_ids:
                        estudiantes = Usuario.objects.filter(email__in=estudiantes_ids, rol='EST')
                        logger.info(f"[DEPURACIÓN] estudiantes encontrados: {[e.email for e in estudiantes]}")
                        if estudiantes.count() != len(estudiantes_ids):
                            logger.warning(f"[DEPURACIÓN] Algunos estudiantes no existen en la BD: {set(estudiantes_ids) - set([e.email for e in estudiantes])}")
                        for estudiante in estudiantes:
                            EntregaTarea.objects.get_or_create(
                                tarea=asignacion,
                                estudiante=estudiante
                            )
                            estudiantes_creados.add(estudiante.email)
                    # Asignar grupos
                    if grupos_ids:
                        grupos = Grupo.objects.filter(id__in=grupos_ids)
                        for grupo in grupos:
                            for estudiante in grupo.estudiantes.all():
                                if estudiante.email not in estudiantes_creados:
                                    EntregaTarea.objects.get_or_create(
                                        tarea=asignacion,
                                        estudiante=estudiante,
                                        grupo=grupo
                                    )
                                    estudiantes_creados.add(estudiante.email)
                return Response({'mensaje': 'Asignación realizada correctamente'}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"[DEPURACIÓN] Error en asignar_estudiantes_grupos: {str(e)}", exc_info=True)
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.error(f"[DEPURACIÓN] Errores de validación: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer
    
    def get_queryset(self):
        queryset = Grupo.objects.all()
        curso_id = self.request.query_params.get('curso_id')
        if curso_id:
            queryset = queryset.filter(curso__id=curso_id)
        return queryset.order_by('nombre')
    
    @action(detail=False, methods=['post'])
    def crear_grupos_aleatorios(self, request):
        # Permitir recibir min_estudiantes en vez de cantidad_grupos
        serializer = CrearGrupoAleatorioSerializer(data=request.data)
        if serializer.is_valid() or ('asignatura_id' in request.data and 'min_estudiantes' in request.data and 'nombre_base' in request.data):
            asignatura_id = request.data.get('asignatura_id') or serializer.validated_data.get('asignatura_id')
            min_estudiantes = int(request.data.get('min_estudiantes', 2))
            nombre_base = request.data.get('nombre_base') or serializer.validated_data.get('nombre_base')
            try:
                asignatura = Asignatura.objects.get(id=asignatura_id)
                from ..models import SolicitudAsignatura, Curso
                curso_objeto = Curso.objects.filter(asignatura=asignatura).first()
                if not curso_objeto:
                    return Response({'error': 'No existe un curso para esta asignatura'}, status=status.HTTP_400_BAD_REQUEST)
                solicitudes = SolicitudAsignatura.objects.filter(asignatura=asignatura, estado='aceptado')
                estudiantes = Usuario.objects.filter(email__in=solicitudes.values_list('estudiante__email', flat=True), rol='EST')
                if estudiantes.count() == 0:
                    return Response(
                        {'error': 'No hay estudiantes inscritos en esta asignatura'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                estudiantes_list = list(estudiantes)
                random.shuffle(estudiantes_list)
                total_estudiantes = len(estudiantes_list)
                # Calcular cantidad de grupos según min_estudiantes
                cantidad_grupos = max(1, (total_estudiantes + min_estudiantes - 1) // min_estudiantes)
                if cantidad_grupos > total_estudiantes:
                    cantidad_grupos = total_estudiantes
                estudiantes_por_grupo = total_estudiantes // cantidad_grupos
                estudiantes_sobrantes = total_estudiantes % cantidad_grupos
                grupos_creados = []
                with transaction.atomic():
                    inicio = 0
                    for i in range(cantidad_grupos):
                        tamaño_grupo = estudiantes_por_grupo
                        if i < estudiantes_sobrantes:
                            tamaño_grupo += 1
                        grupo = Grupo.objects.create(
                            nombre=f"{nombre_base} {i + 1}",
                            curso=curso_objeto,
                            descripcion=f"Grupo creado automáticamente para {asignatura.nombre}"
                        )
                        estudiantes_grupo = estudiantes_list[inicio:inicio + tamaño_grupo]
                        grupo.estudiantes.add(*estudiantes_grupo)
                        grupos_creados.append(grupo)
                        inicio += tamaño_grupo
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
        import logging
        logger = logging.getLogger(__name__)
        grupo = self.get_object()
        estudiante_id = request.data.get('estudiante_id')
        try:
            estudiante = Usuario.objects.get(email=estudiante_id, rol='EST')
            logger.info(f"[DEPURACIÓN] Intentando agregar estudiante {estudiante.email} al grupo {grupo.nombre} (curso: {grupo.curso})")
            grupo.agregar_estudiante(estudiante)
            logger.info(f"[DEPURACIÓN] Estudiante {estudiante.email} agregado correctamente al grupo {grupo.nombre}")
            return Response({'mensaje': 'Estudiante agregado al grupo'}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            logger.error(f"[DEPURACIÓN] Estudiante no encontrado: {estudiante_id}")
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"[DEPURACIÓN] Error al agregar estudiante: {str(e)}", exc_info=True)
            return Response({'error': f'[DEPURACIÓN] {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def remover_estudiante(self, request, pk=None):
        grupo = self.get_object()
        estudiante_id = request.data.get('estudiante_id')
        try:
            estudiante = Usuario.objects.get(email=estudiante_id, rol='EST')
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
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SolicitarAsignaturaViewSet(ViewSet):
    authentication_classes = []  # No usar autenticación automática
    def create(self, request):
        print("Dentro de create")
        try:
            token = request.headers.get('Authorization', None)
            if not token:
                return Response({'error': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

            token = token.split(" ")[1]
            print("Token recibido:", token)
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print('Decoded token:', decoded)  # Debugging line
            email = decoded['email']
            print('Decoded email:', email)  # Debugging line
            estudiante = Usuario.objects.get(email=email)
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

        asignatura_id = request.data.get('asignatura_id')
        try:
            asignatura = Asignatura.objects.get(id=asignatura_id)
        except Asignatura.DoesNotExist:
            return Response({'error': 'Asignatura no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        SolicitudAsignatura.objects.create(
            estudiante=estudiante,
            asignatura=asignatura,
            estado='pendiente'
        )

        return Response({'message': 'Solicitud enviada con éxito'}, status=status.HTTP_201_CREATED)
