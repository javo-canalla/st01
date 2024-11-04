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


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.requester = request.user
            order.save()
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
        orders = Order.objects.filter(assigned_to__isnull=True).order_by('-order_number')
        workers = CustomUser.objects.filter(user_type='worker')
        return render(request, 'orderapp/assign_orders.html', {'orders': orders, 'workers': workers})


@login_required
@user_passes_test(is_supervisor)
def view_orders(request):
    # Obtener el filtro de estado
    status_filter = request.GET.get('status_filter', 'all')

    # Filtrar los pedidos por estado
    if status_filter == 'pending':
        orders = Order.objects.filter(status='pending').order_by('-order_number')
    elif status_filter == 'assigned':
        orders = Order.objects.filter(status='assigned').order_by('-order_number')
    elif status_filter == 'completed':
        orders = Order.objects.filter(status='completed').order_by('-order_number')
    else:
        orders = Order.objects.all().order_by('-order_number')

    # Obtener la lista de trabajadores (usuarios de tipo 'worker')
    workers = CustomUser.objects.filter(user_type='worker')

    # Procesar la solicitud POST para guardar cambios
    if request.method == "POST":
        print("Datos de la solicitud POST:", request.POST)  # Agregar esta línea
        for order in orders:
            worker_id = request.POST.get(f'worker_id_{order.order_number}')
            supervisor_comment = request.POST.get(f'supervisor_comment_{order.order_number}')
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
            print(worker_id)
            print(supervisor_comment)
                    

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
