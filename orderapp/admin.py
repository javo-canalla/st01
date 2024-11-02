# /orderapp/admin.py
from django.contrib import admin
from .models import Order


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'task', 'urgency', 'status',
                    'requester', 'assigned_to', 'order_date', 'end_date')
    list_filter = ('status', 'urgency', 'task')
    search_fields = ('order_number', 'requester__name',
                     'assigned_to__name', 'contact_email')
    ordering = ('-order_date',)


admin.site.register(Order, OrderAdmin)
