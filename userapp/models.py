# /userapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('La dirección de correo es obligatoria')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField('Nombre', max_length=30, blank=True)
    last_name = models.CharField('Apellido', max_length=30, blank=True)
    email = models.EmailField('Dirección de correo', unique=True)
    phone_number = models.CharField(
        'Teléfono propio', max_length=15, blank=True)
    int_phone = models.CharField('Teléfono interno', max_length=10, blank=True)

    USER_TYPE_CHOICES = (
        ('common', 'Común'),
        ('worker', 'Trabajador'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Administrador'),
    )
    user_type = models.CharField(
        'Tipo de usuario', max_length=10, choices=USER_TYPE_CHOICES, default='common')

    receive_order_emails = models.BooleanField(
        default=True,
        verbose_name='Recibir correos de pedidos sin asignación'
    )

    is_active = models.BooleanField('Está activo', default=True)
    is_staff = models.BooleanField('Es personal', default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email y contraseña son requeridos por defecto.

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.email
