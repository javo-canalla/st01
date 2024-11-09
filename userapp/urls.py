# /userapp/urls.py
from django.urls import path
from .views import (
    login, logout, dashboard, register, user_list, delete_user,
    password_change, password_change_done, password_reset, password_reset_done,
    password_reset_confirm, password_reset_complete, save_user_changes,
    workeruser_login,
)


urlpatterns = [
    path('', login, name="login"),
    path('logout/', logout, name="logout"),
    path('dashboard/', dashboard, name="dashboard"),
    path('register/', register, name='register'),
    path('users/', user_list, name='user_list'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('password_change/', password_change, name='password_change'),
    path('password_change/done/', password_change_done,
         name='password_change_done'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/done/', password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm,
         name='password_reset_confirm'),
    path('reset/done/', password_reset_complete,
         name='password_reset_complete'),
    path('save_user_changes/', save_user_changes, name='save_user_changes'),
    path('workeruser/', workeruser_login, name='workeruser_login'),
]
