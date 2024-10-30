# /userapp/forms.py
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, UserChangeForm,
    PasswordChangeForm, PasswordResetForm, SetPasswordForm
)
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
        
class UserEditForm(UserChangeForm):
    password = None  # Ocultar el campo de contraseña

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


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Contraseña anterior"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Dirección de correo"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'autofocus': True}),
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )