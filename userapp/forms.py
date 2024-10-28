# /userapp/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={'autofocus': True}), label=_("Dirección de correo"))
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'last_name', 'phone_number', 'int_phone', 'user_type']
        labels = {
            'email': 'Dirección de correo',
            'name': 'Nombre',
            'last_name': 'Apellido',
            'phone_number': 'Teléfono propio',
            'int_phone': 'Teléfono interno',
            'user_type': 'Tipo de usuario',
        }