# /orderapp/models.py
from django.db import models
from django.conf import settings
# Create your models here.
class Order(models.Model):
    TASK_CHOICES = [
        ('repair_equipment', 'Reparación de equipo'),
        ('install_equipment', 'Instalación de equipo'),
        ('repair_building', 'Reparación edilicia'),
        ('device_manufacture', 'Fabricación de dispositivo'),
        ('informatics_order', 'Pedido a informática'),
    ]
    
    URGENCY_CHOICES = [
        ('normal', 'Normal'),
        ('low', 'Baja'),
        ('high', 'Alta'),
    ]
    
    BILL_TO_CHOICES = [
        ('subsidy', 'Subsidio'),
        ('ibr', 'IBR'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('assigned', 'Asignada'),
        ('completed', 'Finalizada'),
    ]
    
    COMPLETION_PERCENTAGE_CHOICES = [
        (0, '0%'),
        (25, '25%'),
        (50, '50%'),
        (75, '75%'),
        (100, '100%'),
    ]

    task = models.CharField(max_length=20, choices=TASK_CHOICES)
    equipment_type = models.CharField(max_length=100)
    physical_location = models.CharField(max_length=100)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='normal')
    contact_email = models.EmailField()
    serial_number = models.CharField(max_length=50, blank=True)
    conicet_id = models.CharField(max_length=50, blank=True)
    bill_to = models.CharField(max_length=10, choices=BILL_TO_CHOICES)
    detail = models.TextField(blank=True)
    failure_description = models.TextField()
    sworn_statement = models.BooleanField(default=False)
    
    # Campos de control del pedido
    order_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    order_number = models.AutoField(primary_key=True)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'user_type': 'worker'}, related_name='assigned_orders')
    supervisor_comment = models.TextField(blank=True)
    technical_report = models.TextField(blank=True)
    completion_percentage = models.IntegerField(choices=COMPLETION_PERCENTAGE_CHOICES, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Orden #{self.order_number} - {self.task}"
