# /orderapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json
from .forms import OrderForm
from .models import Order
from userapp.models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.requester = request.user
            order.save()

            # Obtener supervisores para enviar notificación
            # Filtrar supervisores que tienen habilitada la recepción de correos
            supervisors = CustomUser.objects.filter(
                user_type='supervisor', receive_order_emails=True)
            supervisor_emails = [
                supervisor.email for supervisor in supervisors]

            # Enviar correo de notificación a los supervisores
            if supervisor_emails:
                subject = 'Nuevo pedido ingresado para asignación'
                message = (
                    f"Ha ingresado un nuevo pedido que necesita ser asignado.\n\n"
                    f"Detalles del pedido:\n"
                    f" - Número de serie: {order.serial_number}\n"
                    f" - Identificación CONICET: {order.conicet_id}\n"
                    f" - Email de contacto: {order.contact_email}\n"
                    f" - Facturar a: {order.get_bill_to_display()}\n"
                    f" - Fecha de finalización: {order.end_date}\n"
                    f" - Detalle: {order.detail}\n"
                    f" - Tipo de tarea: {order.get_task_display()}\n"
                    f" - Interno solicitante: {order.requester.int_phone}\n"
                    f" - Email solicitante: {order.requester.email}\n"
                    f" - Teléfono solicitante: {
                        order.requester.phone_number}\n"
                    f" - Descripción de la falla: {
                        order.failure_description}\n"
                )
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    supervisor_emails,
                    fail_silently=False,
                )

            return redirect('dashboard')
    else:
        form = OrderForm()
    return render(request, 'orderapp/create_order.html', {'form': form})


@csrf_exempt
def update_order_description(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_description = data.get('description')

        try:
            order = Order.objects.get(order_number=order_id)
            order.failure_description = new_description
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Pedido no encontrado.'})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'})


def order_list(request):
    orders = Order.objects.filter(requester=request.user)
    return render(request, 'orderapp/order_list.html', {'orders': orders})


def is_supervisor(user):
    return user.user_type == 'supervisor'


@login_required
@user_passes_test(is_supervisor)
def assign_orders(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('order_id_'):
                order_id = value
                worker_id = request.POST.get(f'worker_id_{order_id}')
                order = Order.objects.get(order_number=order_id)
                if worker_id:  # Asignar al trabajador seleccionado
                    worker = CustomUser.objects.get(id=worker_id)
                    order.assigned_to = worker
                    order.status = 'assigned'
                else:  # Si no hay trabajador seleccionado, dejar sin asignación
                    order.assigned_to = None
                    order.status = 'pending'
                order.save()
        return redirect('dashboard')
    else:
        orders = Order.objects.filter(
            assigned_to__isnull=True).order_by('-order_number')
        workers = CustomUser.objects.filter(
            user_type__in=['worker', 'supervisor'])
        return render(request, 'orderapp/assign_orders.html', {'orders': orders, 'workers': workers})


@login_required
@user_passes_test(is_supervisor)
def view_orders(request):
    # Obtener el filtro de estado
    status_filter = request.GET.get('status_filter', 'all')

    # Filtrar los pedidos por estado
    if status_filter == 'pending':
        orders = Order.objects.filter(
            status='pending').order_by('-order_number')
    elif status_filter == 'assigned':
        orders = Order.objects.filter(
            status='assigned').order_by('-order_number')
    elif status_filter == 'completed':
        orders = Order.objects.filter(
            status='completed').order_by('-order_number')
    else:
        orders = Order.objects.all().order_by('-order_number')

    # Obtener la lista de trabajadores (usuarios de tipo 'worker')
    workers = CustomUser.objects.filter(user_type__in=['worker', 'supervisor'])

    # Procesar la solicitud POST para guardar cambios
    if request.method == "POST":
        for order in orders:
            worker_id = request.POST.get(f'worker_id_{order.order_number}')
            supervisor_comment = request.POST.get(
                f'supervisor_comment_{order.order_number}')
            if worker_id:  # Asignar al trabajador si se seleccionó uno
                order.assigned_to_id = worker_id
                if order.status != 'completed':  # Cambiar a "assigned" si no está completado
                    order.status = 'assigned'
            else:  # Sin asignación, establecer en pendiente si no está completado
                order.assigned_to = None
                if order.status != 'completed':
                    order.status = 'pending'

            if supervisor_comment is not None:
                order.supervisor_comment = supervisor_comment

            order.save()

            # Guardar cualquier cambio realizado en el pedido
            order.save()

        # Mensaje de éxito y redirección
        messages.success(request, 'Cambios guardados correctamente.')
        return redirect('view_orders')

    # Contexto de la plantilla
    context = {
        'orders': orders,
        'workers': workers,
        'selected_status': status_filter,
    }
    return render(request, 'orderapp/view_orders.html', context)


@login_required
def resolve_orders(request):
    # Filtrar pedidos asignados al usuario actual que no estén finalizados
    orders = Order.objects.filter(assigned_to=request.user).exclude(
        status='completed').order_by('-order_number')

    if request.method == 'POST':
        for order in orders:
            completion_percentage = request.POST.get(
                f'completion_{order.order_number}')
            technical_report = request.POST.get(
                f'technical_report_{order.order_number}')

            if completion_percentage is not None:
                order.completion_percentage = int(completion_percentage)
                if order.completion_percentage == 100:
                    order.status = 'completed'

            if technical_report is not None:
                order.technical_report = technical_report

            order.save()

        messages.success(request, 'Cambios guardados correctamente.')
        return redirect('dashboard')

    context = {
        'orders': orders,
        'completion_choices': Order.COMPLETION_PERCENTAGE_CHOICES,
    }
    return render(request, 'orderapp/resolve_orders.html', context)


@login_required
def view_user_orders(request):
    # Obtener filtro de estado desde la solicitud GET (predeterminado: todos)
    status_filter = request.GET.get('status_filter', 'all')
    # Filtrar pedidos según el estado seleccionado y que estén asignados al usuario actual
    orders = Order.objects.filter(
        assigned_to=request.user).order_by('-order_number')

    if status_filter == 'pending':
        orders = orders.filter(status='pending')
    elif status_filter == 'assigned':
        orders = orders.filter(status='assigned')
    elif status_filter == 'completed':
        orders = orders.filter(status='completed')

    if request.method == 'POST':
        for order in orders:
            # Capturar % Realización y Reporte Técnico
            completion_percentage = request.POST.get(
                f'completion_{order.order_number}')
            technical_report = request.POST.get(
                f'technical_report_{order.order_number}')

            if completion_percentage is not None:
                order.completion_percentage = int(completion_percentage)
                # Cambiar estado según el % Realización
                if order.completion_percentage == 100:
                    order.status = 'completed'
                else:
                    order.status = 'assigned'

            if technical_report is not None:
                order.technical_report = technical_report

            order.save()

        messages.success(request, 'Cambios guardados correctamente.')
        return redirect('view_user_orders')

    context = {
        'orders': orders,
        'completion_choices': Order.COMPLETION_PERCENTAGE_CHOICES,
        'selected_status': status_filter,
    }
    return render(request, 'orderapp/view_user_orders.html', context)
