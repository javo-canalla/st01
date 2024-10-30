# /userapp/forms.py
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, UserChangeForm,
    PasswordChangeForm, PasswordResetForm, SetPasswordForm
)
from django.utils.translation import gettext_lazy as _
from .models import CustomUser



class BootstrapFormMixin:
    """Agrega clases Bootstrap a los formularios."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.EmailField(label="Dirección de correo", widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class UserRegisterForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'last_name', 'phone_number', 'int_phone', 'user_type']
        
class UserEditForm(BootstrapFormMixin, UserChangeForm):
    password = None  # Ocultar contraseña en el formulario de edición.
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'last_name', 'phone_number', 'int_phone', 'user_type']


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