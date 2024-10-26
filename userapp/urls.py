from django.urls import path
from .views import login, logout, dashboard, homepage


urlpatterns = [
    path('', homepage, name="homepage"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('dashboard/', dashboard, name="dashboard"),
]
