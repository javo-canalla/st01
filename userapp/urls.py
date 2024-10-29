# /userapp/urls.py
from django.urls import path
from .views import login, logout, dashboard, homepage, register, user_list, edit_user, delete_user
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm


urlpatterns = [
    path('', homepage, name="homepage"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('dashboard/', dashboard, name="dashboard"),
    path('register/', register, name='register'),
    path('users/', user_list, name='user_list'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='userapp/password_change.html',
        form_class=CustomPasswordChangeForm
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='userapp/password_change_done.html'
    ), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='userapp/password_reset.html',
        email_template_name='userapp/password_reset_email.html',
        subject_template_name='userapp/password_reset_subject.txt',
        form_class=CustomPasswordResetForm
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='userapp/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='userapp/password_reset_confirm.html',
        form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='userapp/password_reset_complete.html'
    ), name='password_reset_complete'),
]
