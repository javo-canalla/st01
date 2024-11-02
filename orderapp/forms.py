# /orderapp/forms.py
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'task', 'equipment_type', 'physical_location', 'urgency', 'contact_email',
            'serial_number', 'conicet_id', 'bill_to', 'detail', 'failure_description', 'sworn_statement'
        ]
        labels = {
            'task': 'Tarea',
            'equipment_type': 'Tipo de equipo',
            'physical_location': 'Ubicación física',
            'urgency': 'Urgencia',
            'contact_email': 'Email de contacto',
            'serial_number': 'Número de serie',
            'conicet_id': 'Identificación CONICET',
            'bill_to': 'Facturar a',
            'detail': 'Detalle',
            'failure_description': 'Descripción de la falla',
            'sworn_statement': 'Declaración jurada (El equipo se encuentra libre de contaminación)'
        }
        widgets = {
            'task': forms.Select(attrs={'class': 'form-control'}),
            'equipment_type': forms.TextInput(attrs={'class': 'form-control'}),
            'physical_location': forms.TextInput(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'conicet_id': forms.TextInput(attrs={'class': 'form-control'}),
            'bill_to': forms.Select(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'failure_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'sworn_statement': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
