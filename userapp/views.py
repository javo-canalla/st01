# /userapp/views.py
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import (
    LoginForm, UserRegisterForm, UserEditForm,
    CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
)
from .models import CustomUser


# Create your views here.


def homepage(request):
    return render(request, 'userapp/index.html')


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'loginform': form}
    return render(request, 'userapp/login.html', context=context)


@login_required(login_url="login")
def dashboard(request):
    return render(request, 'userapp/dashboard.html')


def logout(request):
    auth.logout(request)
    return redirect("homepage")


def is_admin_user(user):
    return user.user_type == 'admin'

@user_passes_test(is_admin_user, login_url='login')
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'userapp/register.html', context)

@user_passes_test(is_admin_user, login_url='login')
def user_list(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'userapp/user_list.html', context)

@user_passes_test(is_admin_user, login_url='login')
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)
    context = {'form': form}
    return render(request, 'userapp/edit_user.html', context)

@user_passes_test(is_admin_user, login_url='login')
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user == request.user:
        messages.error(request, 'No puede eliminar su propio usuario.')
        return redirect('user_list')
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('user_list')
    context = {'user': user}
    return render(request, 'userapp/delete_user.html', context)

@login_required(login_url="login")
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para mantener la sesión
            messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
            return redirect('password_change_done')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'userapp/password_change.html', context)

@login_required(login_url="login")
def password_change_done(request):
    return render(request, 'userapp/password_change_done.html')

def password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = 'Solicitud de restablecimiento de contraseña'
                    email_template_name = 'userapp/password_reset_email.html'
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Mi Sitio',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_body = render_to_string(email_template_name, c)
                    send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.')
                return redirect('password_reset_done')
            else:
                messages.error(request, 'No existe ninguna cuenta registrada con esa dirección de correo.')
    else:
        form = CustomPasswordResetForm()
    context = {'form': form}
    return render(request, 'userapp/password_reset.html', context)

def password_reset_done(request):
    return render(request, 'userapp/password_reset_done.html')

def password_reset_confirm(request, uidb64=None, token=None):
    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tu contraseña ha sido restablecida exitosamente.')
                return redirect('password_reset_complete')
        else:
            form = CustomSetPasswordForm(user)
        context = {'form': form}
        return render(request, 'userapp/password_reset_confirm.html', context)
    else:
        messages.error(request, 'El enlace de restablecimiento de contraseña no es válido o ha expirado.')
        return redirect('password_reset')

def password_reset_complete(request):
    return render(request, 'userapp/password_reset_complete.html')