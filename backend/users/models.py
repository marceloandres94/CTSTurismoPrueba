from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    """
    Manager personalizado para el modelo de usuario que extiende BaseUserManager.
    Contiene los métodos para crear usuarios normales y superusuarios.
    """

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Crea y guarda un usuario regular con el email y contraseña dados.
        """
        if not email:
            raise ValueError('El email es requerido')
        
        # Normalizamos el email para evitar inconsistencias
        email = self.normalize_email(email)
        
        # Validamos el email
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            raise ValueError('El email proporcionado no es válido')
        
        # Configuración del usuario como no administrativo
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        # Crear el usuario
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)  # Configurar la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con permisos de administrador.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True')

        return self.create_user(email, first_name, last_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado que extiende AbstractBaseUser y PermissionsMixin.
    Utiliza el campo 'email' como identificador principal en lugar de 'username'.
    """

    email = models.EmailField(
        unique=True,
        max_length=255,
        validators=[EmailValidator()],
        error_messages={'unique': "Ya existe un usuario con este correo."}
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)  # Se activará tras la verificación del email
    is_staff = models.BooleanField(default=False)   # Los usuarios no administrativos no tienen acceso de staff
    date_joined = models.DateTimeField(default=timezone.now)

    # Asignamos nuestro UserManager personalizado como el manager de este modelo
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def clean(self):
        """
        Validaciones personalizadas que se ejecutarán antes de guardar el modelo.
        """
        if not self.first_name:
            raise ValidationError('El nombre es obligatorio.')
        if not self.last_name:
            raise ValidationError('El apellido es obligatorio.')

    def save(self, *args, **kwargs):
        """
        Sobreescribe el método save para agregar validaciones personalizadas si es necesario.
        """
        self.full_clean()  # Ejecuta la validación personalizada antes de guardar
        super(User, self).save(*args, **kwargs)
