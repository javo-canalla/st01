# /userapp/views.py
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegisterForm



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