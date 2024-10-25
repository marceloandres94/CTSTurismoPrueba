from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializador para el registro de usuarios. Valida el email y crea usuarios,
    enviando un email de verificación tras el registro.
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def validate_email(self, value):
        """
        Valida que el email sea único antes de crear el usuario.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este correo electrónico ya está registrado.')
        return value

    def create(self, validated_data):
        # Crear usuario sin contraseña inicial y con el estado inactivo
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_unusable_password()  # La contraseña se establecerá después de la verificación
        user.is_active = False        # La cuenta está inactiva hasta la verificación de correo
        user.save()
        return user

class SetPasswordSerializer(serializers.Serializer):
    """
    Serializador para permitir a los usuarios establecer una nueva contraseña.
    """
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        """
        Valida la contraseña utilizando las reglas de Django.
        """
        try:
            validate_password(value)  # Aplica las validaciones estándar de Django
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)  # Devuelve mensajes de error específicos
        return value

    def save(self, user):
        # Guarda la nueva contraseña en el usuario proporcionado
        user.set_password(self.validated_data['password'])
        user.save()

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializador para listar usuarios con campos seleccionados.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff', 'date_joined']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador personalizado para JWT que incluye la validación de is_staff y is_superuser.
    """
    def validate(self, attrs):
        credentials = {
            'email': attrs.get("email"),
            'password': attrs.get("password")
        }
        user = authenticate(**credentials)
        if user:
            if user.is_superuser and user.is_staff:
                data = super().validate(attrs)
                data.update({'is_superuser': user.is_superuser, 'is_staff': user.is_staff})
                return data
            else:
                raise serializers.ValidationError("No tienes permisos para acceder al panel de administración.")
        raise serializers.ValidationError("Credenciales inválidas.")
