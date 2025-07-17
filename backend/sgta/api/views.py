from rest_framework import viewsets
from ..core.domain import *
from .serializers import UsuarioSerializer, AsignaturaSerializer,PeriodoLectivoSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
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

class PeriodoLectivoViewSet(viewsets.ModelViewSet):
    queryset = PeriodoLectivo.objects.all()
    serializer_class = PeriodoLectivoSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data['nombre']
            contrasenia = serializer.validated_data['contrasenia']

            try:
                user = Usuario.objects.get(nombre=nombre)
                if check_password(contrasenia, user.contrasenia):
                    payload = {
                        'id': user.id,
                        'email': user.email,
                        'rol': user.rol,
                        'exp': datetime.utcnow() + timedelta(minutes=30),
                        'iat': datetime.utcnow(),
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                    return Response({'access': token})
                return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)