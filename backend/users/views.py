from django.shortcuts import render
from rest_framework import generics, status
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserListSerializer,
    SetPasswordSerializer,
    CustomTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from rest_framework.response import Response
from rest_framework.views import APIView
from random import choice
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from .permissions import IsSuperUser  # Importa el permiso personalizado
import random

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener el token JWT utilizando CustomTokenObtainPairSerializer
    que agrega is_superuser e is_staff en la respuesta de autenticación.
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    Vista para registrar nuevos usuarios, quienes reciben un email de verificación tras el registro.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False  # La cuenta estará inactiva hasta que se verifique el email
        user.save()
        self.send_verification_email(user)

    def send_verification_email(self, user):
        """
        Envia un email de verificación al usuario registrado.
        """
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = f'http://localhost:8080/verify/{uid}/{token}'

        send_mail(
            'Verificación de correo electrónico',
            f'Haz clic en el siguiente enlace para verificar tu correo: {verification_link}',
            'no-reply@hotel.com',
            [user.email],
            fail_silently=False,
        )

class EmailVerificationView(APIView):
    """
    Verifica el correo del usuario a través de un enlace que activa la cuenta y permite la configuración de contraseña.
    """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Correo verificado correctamente. Ahora puedes establecer tu contraseña.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)

class SetPasswordView(generics.UpdateAPIView):
    """
    Permite a los usuarios establecer una nueva contraseña después de verificar su email.
    """
    serializer_class = SetPasswordSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'put', 'patch']

    def get_object(self):
        uid = self.request.data.get('uid')
        token = self.request.data.get('token')
        
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise Response({"error": "Usuario no válido"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            raise Response({"error": "Token no válido o expirado"}, status=status.HTTP_400_BAD_REQUEST)

        return user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"message": "Contraseña establecida exitosamente."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SelectWinnerView(APIView):
    """
    Vista accesible solo para superusuarios que permite seleccionar un ganador del sorteo.
    """
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        # Solo considera usuarios activos que no sean staff ni superuser
        users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)
        if users.exists():
            winner = random.choice(users)
            send_mail(
                '¡Felicidades! Has ganado una estadía de 2 noches',
                f'Hola {winner.first_name}, ¡has sido seleccionado como el ganador de nuestro sorteo!',
                'no-reply@hotel.com',
                [winner.email],
                fail_silently=False,
            )
            return Response({'message': f'El ganador es: {winner.first_name} {winner.last_name}<br>Correo: {winner.email}'})

        return Response({'message': 'No hay usuarios inscritos'}, status=400)

class UserListView(generics.ListAPIView):
    """
    Lista todos los usuarios registrados.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]
