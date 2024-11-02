# /orderapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import json
from .forms import OrderForm
from .models import Order


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
