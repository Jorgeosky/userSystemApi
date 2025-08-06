from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    # La contraseña es solo de lectura, pero en el POST debe ser proporcionada
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'voucher']  # Asegúrate de que estos campos sean correctos
    
    def validate_password(self, value):
        # Se puede agregar validación de contraseñas si es necesario
        validate_password(value)
        return value

    def create(self, validated_data):
        # Crea el usuario y asigna la contraseña de forma segura
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Usa `set_password` para asegurar la contraseña
        user.save()
        return user