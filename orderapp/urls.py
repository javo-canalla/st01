# /orderapp/urls.py
from django.urls import path
from .views import create_order, order_list, update_order_description, assign_orders, view_orders, resolve_orders, view_user_orders

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('list/', order_list, name='order_list'),
    path('update-description/', update_order_description,
         name='update_order_description'),
    path('assign-orders/', assign_orders, name='assign_orders'),
    path('view-orders/', view_orders, name='view_orders'),
    path('resolve-orders/', resolve_orders, name='resolve_orders'),
    path('view-user-orders/', view_user_orders, name='view_user_orders'),
]
