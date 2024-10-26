# /userapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'last_name', 'user_type', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {
         'fields': ('name', 'last_name', 'phone_number', 'int_phone')}),
        ('Permisos', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'user_type', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
