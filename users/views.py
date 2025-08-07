from rest_framework import status, permissions, viewsets
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
import string
import random
import base64
from datetime import datetime

# Función para generar un código alfanumérico aleatorio de 8 caracteres
def generate_voucher_code():
    characters = string.ascii_uppercase + string.digits  # Letras mayúsculas y números
    voucher_code = ''.join(random.choice(characters) for i in range(8))
    return voucher_code

# Función para obtener la fecha y hora actual en Base64
def get_base64_datetime():
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora en formato: 'YYYY-MM-DD HH:MM:SS'
    encoded_datetime = base64.b64encode(current_datetime.encode('utf-8')).decode('utf-8')
    return encoded_datetime


from .models import CustomUser
from .serializers import UserSerializer

def generate_voucher_code():
    characters = string.ascii_uppercase + string.digits  # Letras mayúsculas y números
    voucher_code = ''.join(random.choice(characters) for i in range(8))
    return voucher_code

def get_base64_datetime():
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Fecha y hora en formato: 'YYYY-MM-DD HH:MM:SS'
    encoded_datetime = base64.b64encode(current_datetime.encode('utf-8')).decode('utf-8')
    return encoded_datetime

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Sobrescribimos el método get_permissions para que los usuarios solo puedan
        actualizar sus propios perfiles, a menos que sean administradores.
        """
        if self.action in ['update', 'partial_update']:
            # Si el usuario no es el mismo que el usuario que se está editando
            if self.request.user.id != int(self.kwargs['pk']) and self.request.user.role != 'admin':
                raise PermissionDenied("No tienes permiso para editar este usuario.")
        return super().get_permissions()

    def perform_create(self, serializer):
        # Validar si el rol es correcto antes de crear el usuario
        role = serializer.validated_data.get('role')
        if role not in ['admin', 'user']:
            raise serializers.ValidationError("Invalid role.")
        serializer.save()

    def perform_update(self, serializer):
        # Validar si el rol es correcto antes de actualizar el usuario
        role = serializer.validated_data.get('role')
        if role not in ['admin', 'user']:
            raise serializers.ValidationError("Invalid role.")
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not self.request.user.is_authenticated:
            raise PermissionDenied("No estás autenticado.")
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
        # Solo validamos el rol si está presente en los datos de la solicitud
        role = data.get('role', None)
        print(role)
        if role and role not in ['admin', 'user']:
            raise serializers.ValidationError("Invalid role.")
        
        # Guardamos los cambios
        serializer.save()

    def perform_patch(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("No estás autenticado.")

        data = serializer.validated_data
        
        # Solo validamos el rol si está presente en los datos de la solicitud
        role = data.get('role', None)
        print(role)
        if role and role not in ['admin', 'user']:
            raise serializers.ValidationError("Invalid role.")
        
        # Guardamos los cambios
        serializer.save()

    @action(detail=True, methods=['post'])
    def assign_voucher(self, request, pk=None):
        """
        Endpoint para asignar un voucher a un usuario.
        Solo el administrador o el usuario mismo puede asignar un voucher.
        """
        user = self.get_object()  # Obtiene el usuario especificado por `pk`
        
        # Verificar si el usuario tiene permisos para asignar un voucher
        if request.user.id != user.id and request.user.role != 'admin':
            raise PermissionDenied("No tienes permiso para asignar un voucher a este usuario.")

        # Generar el código del voucher y la fecha en Base64
        voucher_code = generate_voucher_code()
        voucher_datetime = get_base64_datetime()

        # Concatenar el código del voucher y la fecha en Base64 en un solo campo
        combined_voucher = f"{voucher_code}|{voucher_datetime}"

        # Asignar el valor concatenado al campo voucher del usuario
        user.voucher = combined_voucher
        user.save()

        # Responder con el código del voucher asignado y la fecha en Base64
        return Response(
            {"detail": f"Voucher {voucher_code} asignado a {user.username} con fecha {voucher_datetime}"},
            status=status.HTTP_201_CREATED
        )
    # Sobrescribimos el método 'list' para que sea accesible en '/api/users/'
    def list(self, request, *args, **kwargs):
        """
        Sobrescribimos el método `list` para que se acceda en `/api/users/` y no en `/api/users/get_users/`
        """
        self.permission_classes = [permissions.AllowAny]
        queryset = CustomUser.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Sobrescribimos `destroy` para permitir que un usuario elimine su propio perfil
        o un administrador pueda eliminar cualquier usuario.
        """
        instance = self.get_object()

        # Verificar si el usuario tiene permisos para eliminar
        if self.request.user.id != instance.id and self.request.user.role != 'admin':
            raise PermissionDenied("No tienes permiso para eliminar este usuario.")

        # Eliminar al usuario
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
