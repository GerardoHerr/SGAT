from rest_framework import viewsets
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.views import APIView
from ..core.domain.GestionAcademica.curso import Curso
from ..core.domain.GestionTarea.asignacion import Asignacion
import tempfile

# Importar los modelos necesarios desde domain
from ..core.domain.GestionAcademica.solicitudAsignatura import SolicitudAsignatura
from ..core.domain.GestionAcademica.entregarTarea import EntregaTarea
from ..core.domain.GestionAcademica.asignatura import Asignatura
from ..core.domain.GestionTarea.asignacion import Asignacion
from ..core.domain.GestionAcademica.periodo_lectivo import PeriodoLectivo
from ..core.domain.GestionAcademica.inscripcion import Inscripcion
from ..core.domain.GestionTarea.grupo import Grupo
from ..core.domain.GestionAcademica.curso import Curso
from ..core.domain.Autenticacion.usuario import Usuario

from .serializers import UsuarioSerializer, AsignaturaSerializer,PeriodoLectivoSerializer, LoginSerializer, AsignacionSerializer, GrupoSerializer, CrearGrupoAleatorioSerializer, AsignarTareaSerializer, InscripcionSerializer, InscripcionSerializer, AsignarDocenteSerializer, SolicitudAsignaturaSerializer, CursoSerializer, EntregaTareaSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
import jwt
from rest_framework.viewsets import ViewSet
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
import random
from django.db import transaction
from rest_framework.authentication import BasicAuthentication

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
    
    @action(detail=False, methods=['get', 'put', 'delete'], url_path='by-email')
    def get_by_email(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email requerido'}, status=400)

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=404)

        # GET
        if request.method == 'GET':
            serializer = self.get_serializer(usuario)
            return Response(serializer.data)

        # PUT (actualizar)
        elif request.method == 'PUT':
            data = request.data.copy()
            if 'contrasenia' in data and data['contrasenia']:
                data['contrasenia'] = make_password(data['contrasenia'])
            else:
                data['contrasenia'] = usuario.contrasenia  # Mantener la existente

            serializer = self.get_serializer(usuario, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # DELETE
        elif request.method == 'DELETE':
            usuario.delete()
            return Response({'mensaje': 'Usuario eliminado correctamente'}, status=204)
    
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
                from ..core.domain.GestionAcademica.solicitudAsignatura import SolicitudAsignatura
                from ..core.domain.GestionAcademica.curso import Curso
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

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            contrasenia = serializer.validated_data['contrasenia']

            try:

                user = Usuario.objects.get(email=email)
                # Verificar contraseña (comparación directa ya que están en texto plano)
                if check_password(contrasenia, user.contrasenia):
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
    

# Opción 1: ModelViewSet completo para SolicitudAsignatura
class SolicitarAsignaturaViewSet(viewsets.ModelViewSet):
    queryset = SolicitudAsignatura.objects.all()
    serializer_class = SolicitudAsignaturaSerializer
    authentication_classes = []  # No usar autenticación automática
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Requiere token en header para saber el estudiante
        try:
            token = request.headers.get('Authorization', None)
            if not token:
                return Response({'error': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)
            token = token.split(" ")[1]
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = decoded['email']
            estudiante = Usuario.objects.get(email=email)
        except Exception as e:
            print("Error decodificando token:", e)
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

        asignatura_id = request.data.get('asignatura') or request.data.get('asignatura_id')
        if not asignatura_id:
            return Response({'error': 'Falta el id de la asignatura'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            asignatura = Asignatura.objects.get(id=asignatura_id)
        except Asignatura.DoesNotExist:
            return Response({'error': 'Asignatura no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        solicitud = SolicitudAsignatura.objects.create(
            estudiante=estudiante,
            asignatura=asignatura,
            estado='pendiente'
        )
        serializer = self.get_serializer(solicitud)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """Actualiza el estado de una solicitud y asigna tareas si es aceptada"""
        from django.core.files.base import ContentFile
        from ..core.domain.GestionTarea.asignacion import Asignacion
        from ..core.domain.GestionAcademica.entregarTarea import EntregaTarea
        from ..core.domain.GestionAcademica.curso import Curso
        from rest_framework.response import Response
        from rest_framework import status
        
        try:
            solicitud = self.get_object()
            nuevo_estado = request.data.get('estado')

            if nuevo_estado not in ['aceptada', 'rechazada']:
                return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)

            # Si la solicitud está siendo aceptada y no estaba ya aceptada
            if nuevo_estado == 'aceptada' and solicitud.estado != 'aceptada':
                # Obtener todos los cursos para esta asignatura
                cursos = Curso.objects.filter(asignatura=solicitud.asignatura)
                
                for curso in cursos:
                    # Agregar estudiante al curso si no está ya inscrito
                    if not curso.estudiantes.filter(email=solicitud.estudiante.email).exists():
                        curso.estudiantes.add(solicitud.estudiante)
                    
                    # Obtener todas las tareas existentes para este curso
                    tareas = Asignacion.objects.filter(curso=curso)
                    
                    # Crear entregas para cada tarea
                    for tarea in tareas:
                        # Verificar si ya existe una entrega para esta tarea y estudiante
                        if not EntregaTarea.objects.filter(
                            tarea=tarea, 
                            estudiante=solicitud.estudiante
                        ).exists():
                            # Crear un archivo temporal vacío
                            empty_file = ContentFile(b'', name='temporal.txt')
                            
                            # Crear la entrega de tarea
                            # No incluimos 'curso' ya que no es un campo del modelo
                            # La relación con el curso ya está a través de tarea.curso
                            EntregaTarea.objects.create(
                                tarea=tarea,
                                estudiante=solicitud.estudiante,
                                archivo=empty_file,
                                calificacion=None,
                                observaciones='',
                                grupo=None  # Se asigna None por defecto, se actualizará si es grupal
                            )
            
            # Actualizar el estado de la solicitud
            solicitud.estado = nuevo_estado
            solicitud.save()
            
            return Response({'message': 'Estado actualizado y estudiante agregado al curso'})
            
        except SolicitudAsignatura.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        try:
            token = request.headers.get('Authorization', None)
            print("Token recibido:", token)
            if not token:
                return Response({'error': 'Token no proporcionado'}, status=status.HTTP_401_UNAUTHORIZED)

            token = token.split(" ")[1]
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = decoded['email']
            rol = decoded.get('rol')  # Suponiendo que el rol viene en el token
            print("Email del usuario:", email)
            print("Rol del usuario:", rol)

            usuario = Usuario.objects.get(email=email)

            if rol == 'DOC':
                # El usuario es docente, mostramos solicitudes hacia sus asignaturas
                asignaturasDocente = Asignatura.objects.filter(docente_responsable_id=usuario.email)
                solicitudes = SolicitudAsignatura.objects.filter(asignatura__id__in=asignaturasDocente.values_list('id', flat=True))

            elif rol == 'EST':
                # El usuario es estudiante, mostramos sus propias solicitudes
                solicitudes = SolicitudAsignatura.objects.filter(estudiante=usuario.email)

            else:
                return Response({'error': 'Rol no autorizado'}, status=status.HTTP_403_FORBIDDEN)

            serializer = SolicitudAsignaturaSerializer(solicitudes, many=True)
            print("Solicitudes obtenidas:", serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expirado'}, status=status.HTTP_401_UNAUTHORIZED)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Error:", e)
            return Response({'error': 'Error al obtener solicitudes'}, status=status.HTTP_400_BAD_REQUEST)

class CursoViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get'], url_path='por-estudiante')
    def cursos_por_estudiante(self, request):
        """Devuelve los cursos en los que está inscrito el estudiante con el email dado."""
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Se requiere el email del estudiante'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            estudiante = Usuario.objects.get(email=email, rol='EST')
        except Usuario.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        # Buscar cursos donde el estudiante está inscrito
        cursos = Curso.objects.filter(estudiantes__email=estudiante.email).distinct()
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    permission_classes = [AllowAny]
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def get_queryset(self):
        import logging
        logger = logging.getLogger(__name__)
        logger.info("[CURSOS] Iniciando get_queryset para cursos")
        queryset = Curso.objects.all()
        docente_email = self.request.query_params.get('docente_email', None)
        logger.info(f"[CURSOS] Param docente_email: {docente_email}")
        if docente_email:
            try:
                docente = Usuario.objects.get(email=docente_email, rol='DOC')
                logger.info(f"[CURSOS] Docente encontrado: {docente.email}")
                queryset = queryset.filter(docente=docente)
                logger.info(f"[CURSOS] Cursos filtrados por docente: {list(queryset)}")
            except Usuario.DoesNotExist:
                logger.warning(f"[CURSOS] Docente no encontrado: {docente_email}")
                return Curso.objects.none()
            except Exception as e:
                logger.error(f"[CURSOS] Error inesperado buscando docente: {e}", exc_info=True)
                return Curso.objects.none()

        # Intentar obtener usuario autenticado por token
        user = None
        try:
            token = self.request.headers.get('Authorization', None)
            logger.info(f"[CURSOS] Token recibido: {token}")
            if token:
                import jwt
                from django.conf import settings
                token = token.split(" ")[-1]
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                email = decoded.get('email')
                logger.info(f"[CURSOS] Email decodificado del token: {email}")
                if email:
                    user = Usuario.objects.get(email=email)
                    logger.info(f"[CURSOS] Usuario autenticado: {user.email}, rol: {user.rol}")
        except Exception as e:
            logger.warning(f"[CURSOS] Error decodificando token o usuario: {e}", exc_info=True)
            user = None

        # Si el usuario autenticado es estudiante, filtrar solo cursos aceptados
        if user and getattr(user, 'rol', None) == 'EST':
            try:
                from ..core.domain.GestionAcademica.solicitudAsignatura import SolicitudAsignatura
                solicitudes_aceptadas = SolicitudAsignatura.objects.filter(estudiante=user, estado='aceptado')
                asignaturas_aceptadas = [s.asignatura for s in solicitudes_aceptadas]
                queryset = queryset.filter(asignatura__in=asignaturas_aceptadas)
                logger.info(f"[CURSOS] Filtrando cursos para estudiante {user.email}, asignaturas aceptadas: {asignaturas_aceptadas}")
            except Exception as e:
                logger.error(f"[CURSOS] Error filtrando cursos para estudiante: {e}", exc_info=True)
                return Curso.objects.none()

        logger.info(f"[CURSOS] Cursos retornados finales: {list(queryset)}")
        return queryset

    @action(detail=False, methods=['get'])
    def mis_cursos(self, request):
        """Obtener cursos del docente autenticado"""
        docente_email = request.query_params.get('email')
        if not docente_email:
            return Response(
                {'error': 'Se requiere el email del docente'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            docente = Usuario.objects.get(email=docente_email, rol='DOC')
            cursos = Curso.objects.filter(docente_id=docente.email)
            serializer = CursoSerializer(cursos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Docente no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def asignar_docente(self, request):
        """Asignar un docente responsable a un curso"""
        try:
            curso_id = request.data.get('curso_id')
            docente_id = request.data.get('docente_id')  # Este sera el email del docente

            if not curso_id or not docente_id:
                return Response(
                    {'error': 'Se requieren curso_id y docente_id'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            curso = Curso.objects.get(id=curso_id)
            docente = Usuario.objects.get(email=docente_id, rol='DOC')  # Buscar por email

            curso.docente_id = docente.email
            curso.save()

            return Response({
                'mensaje': f'Docente {docente.nombre} {docente.apellido} asignado a {curso.asignatura.nombre}',
                'curso': CursoSerializer(curso).data
            }, status=status.HTTP_200_OK)

        except Curso.DoesNotExist:
            return Response({'error': 'Curso no encontrado'}, status=status.HTTP_404_NOT_FOUND)
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

    @action(detail=True, methods=['get'])
    def estudiantes(self, request, pk=None):
        """Obtener los estudiantes inscritos en un curso específico"""
        try:
            curso = self.get_object()
            estudiantes = curso.estudiantes.all()
            serializer = UsuarioSerializer(estudiantes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Curso.DoesNotExist:
            return Response({'error': 'Curso no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class EntregaTareaViewSet(viewsets.ModelViewSet):
    queryset = EntregaTarea.objects.all()
    serializer_class = EntregaTareaSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        """Agregar el request al contexto del serializador para generar URLs absolutas."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def calificar(self, request, pk=None):
        """
        Permite calificar una entrega de tarea y adjuntar retroalimentación. SIN autenticación.
        """
        from django.utils import timezone
        try:
            entrega = self.get_object()
            tarea = entrega.tarea
            calificacion = request.data.get('calificacion')
            observaciones = request.data.get('observaciones', '')
            retroalimentacion_archivo = request.FILES.get('retroalimentacion_archivo')

            if calificacion is None and not observaciones and not retroalimentacion_archivo:
                return Response(
                    {'error': 'Debe proporcionar al menos una calificación, observaciones o archivo de retroalimentación.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if calificacion is not None:
                try:
                    calificacion = float(calificacion)
                except (ValueError, TypeError):
                    return Response(
                        {'error': 'La calificación debe ser un número válido.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                tipo = tarea.tipo_tarea
                if tipo in ['ACD', 'AA']:
                    max_calif = 2.0
                elif tipo == 'APE':
                    max_calif = 2.5
                else:
                    max_calif = 2.5
                if not (0 <= calificacion <= max_calif):
                    return Response(
                        {'error': f'La calificación debe estar entre 0 y {max_calif} para tareas tipo {tipo}.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                entrega.calificacion = calificacion

            if retroalimentacion_archivo:
                if entrega.retroalimentacion_archivo:
                    entrega.retroalimentacion_archivo.delete(save=False)
                entrega.retroalimentacion_archivo = retroalimentacion_archivo

            if observaciones:
                entrega.observaciones = observaciones

            entrega.fecha_retroalimentacion = timezone.now()
            entrega.save()
            serializer = self.get_serializer(entrega)
            return Response(
                {'mensaje': 'Calificación registrada correctamente', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Error al procesar la solicitud: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def partial_update(self, request, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        instance = self.get_object()
        archivo = request.data.get('archivo', None)
        # Si el usuario quiere borrar el archivo
        if archivo == '' or archivo is None:
            try:
                logger.info(f"[ENTREGA] Solicitando borrado de archivo para entrega {instance.id}")
                if hasattr(instance, 'archivo') and instance.archivo:
                    logger.info(f"[ENTREGA] Archivo actual: {instance.archivo}")
                    instance.archivo.delete(save=False)  # Borra el archivo físico
                else:
                    logger.warning(f"[ENTREGA] No hay archivo para borrar en entrega {instance.id}")
                instance.archivo = None
                instance.save()
                serializer = self.get_serializer(instance)
                logger.info(f"[ENTREGA] Archivo borrado correctamente para entrega {instance.id}")
                return Response(serializer.data)
            except Exception as e:
                logger.error(f"[ENTREGA] Error al borrar archivo en entrega {instance.id}: {e}", exc_info=True)
                return Response({'error': f'Error al borrar archivo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Si la tarea es grupal
        tarea = instance.tarea  # Asignacion
        if hasattr(tarea, 'es_grupal') and tarea.es_grupal:
            grupo = getattr(instance, 'grupo', None)
            if grupo:
                integrantes = grupo.estudiantes.all()
                for integrante in integrantes:
                    entrega, created = self.queryset.model.objects.get_or_create(
                        tarea=tarea,
                        estudiante=integrante,
                        grupo=grupo
                    )
                    # Actualiza archivo y fecha para todos
                    if 'archivo' in request.FILES:
                        entrega.archivo = request.FILES['archivo']
                    from django.utils import timezone
                    entrega.fecha_entregada = timezone.now()
                    entrega.save()
                return Response({'mensaje': 'Entrega subida para todo el grupo'}, status=status.HTTP_200_OK)
            else:
                # Si no hay grupo, solo actualiza la entrega individual
                return super().partial_update(request, *args, **kwargs)
        else:
            # Si no es grupal, solo actualiza la entrega individual
            return super().partial_update(request, *args, **kwargs)
    queryset = EntregaTarea.objects.all()
    serializer_class = EntregaTareaSerializer

    def get_queryset(self):
        queryset = EntregaTarea.objects.all()
        tarea_id = self.request.query_params.get('tarea_id')
        if tarea_id:
            queryset = queryset.filter(tarea__id=tarea_id)
        return queryset

class ReporteTareasCursoPDFView(APIView):
    def get(self, request, *args, **kwargs):
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        import io

        curso_id = request.query_params.get('curso')
        tipo = request.query_params.get('tipo', 'tareas')  # 'tareas' o 'entregas'
        if not curso_id:
            return HttpResponse('Curso no especificado', status=400)
        try:
            curso = Curso.objects.get(pk=curso_id)
        except Curso.DoesNotExist:
            return HttpResponse('Curso no encontrado', status=404)
        tareas = Asignacion.objects.filter(curso_id=curso_id)
        docente = getattr(curso, 'docente', None)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        if tipo == 'entregas':
            elements.append(Paragraph(f"Reporte de Entregas de Tareas", styles['Title']))
        else:
            elements.append(Paragraph(f"Reporte de Tareas del Curso", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Curso: {curso}", styles['Heading2']))
        if docente:
            elements.append(Paragraph(f"Docente: {docente}", styles['Normal']))
        elements.append(Spacer(1, 12))

        if tipo == 'entregas':
            from datetime import datetime
            import pytz
            # Por cada tarea, mostrar entregas
            for tarea in tareas:
                elements.append(Paragraph(f"Tarea: {getattr(tarea, 'titulo', '')}", styles['Heading3']))
                entregas = EntregaTarea.objects.filter(tarea=tarea)
                # Cambiar nombre de columna y agregar tiempo restante
                data = [["Estudiante", "Email", "Calificación", "Fecha entregada", "Tiempo restante"]]
                fecha_entrega_obj = getattr(tarea, 'fecha_entrega', None)
                for entrega in entregas:
                    estudiante = getattr(entrega, 'estudiante', None)
                    estudiante_nombre = getattr(estudiante, 'nombre', '') if estudiante else ''
                    estudiante_email = getattr(estudiante, 'email', '') if estudiante else ''
                    calificacion = getattr(entrega, 'calificacion', '')
                    fecha_obj = getattr(entrega, 'fecha_entregada', None)
                    if fecha_obj:
                        fecha_entregada = fecha_obj.strftime('%d/%m/%Y %H:%M')
                    else:
                        fecha_entregada = ''
                    # Calcular tiempo restante
                    tiempo_restante = ''
                    if fecha_entrega_obj:
                        # Convertir a datetime si es necesario
                        now = datetime.now(pytz.UTC) if hasattr(fecha_entrega_obj, 'tzinfo') else datetime.now()
                        if hasattr(fecha_entrega_obj, 'tzinfo'):
                            delta = fecha_entrega_obj - now
                        else:
                            delta = fecha_entrega_obj - datetime.now()
                        if delta.total_seconds() > 0:
                            dias = delta.days
                            horas, resto = divmod(delta.seconds, 3600)
                            minutos = resto // 60
                            tiempo_restante = f"{dias}d {horas}h {minutos}m"
                        else:
                            tiempo_restante = "Finalizado"
                    data.append([
                        estudiante_nombre,
                        estudiante_email,
                        calificacion,
                        fecha_entregada,
                        tiempo_restante
                    ])
                table = Table(data, repeatRows=1)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 18))
        else:
            # Tabla de tareas
            data = [["Título", "Descripción", "Fecha de creación", "Fecha de entrega"]]
            for tarea in tareas:
                # Formatear fechas si existen
                fecha_creacion_obj = getattr(tarea, 'fecha_creacion', None)
                if fecha_creacion_obj:
                    fecha_creacion = fecha_creacion_obj.strftime('%d/%m/%Y %H:%M')
                else:
                    fecha_creacion = ''
                fecha_entrega_obj = getattr(tarea, 'fecha_entrega', None)
                if fecha_entrega_obj:
                    fecha_entrega = fecha_entrega_obj.strftime('%d/%m/%Y %H:%M')
                else:
                    fecha_entrega = ''
                data.append([
                    str(getattr(tarea, 'titulo', '')),
                    str(getattr(tarea, 'descripcion', '')),
                    fecha_creacion,
                    fecha_entrega
                ])
            table = Table(data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        nombre = f"reporte_{'entregas' if tipo == 'entregas' else 'tareas'}_{curso_id}.pdf"
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response