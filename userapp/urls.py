# /userapp/urls.py
from django.urls import path
from .views import login, logout, dashboard, homepage, register, user_list, edit_user, delete_user


urlpatterns = [
    path('', homepage, name="homepage"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('dashboard/', dashboard, name="dashboard"),
    path('register/', register, name='register'),
    path('users/', user_list, name='user_list'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
]
