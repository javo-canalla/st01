# /orderapp/urls.py
from django.urls import path
from .views import create_order, order_list, update_order_description

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('list/', order_list, name='order_list'),
    path('update-description/', update_order_description,
         name='update_order_description'),
]
