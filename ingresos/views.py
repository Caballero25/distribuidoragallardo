from decimal import Decimal
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cuentasporcobrar.models import CuentaPorCobrar
from .models import Ingreso
from django.http import HttpResponse

@login_required

@login_required
def create_ingreso(request, cuenta_id):
    if request.method == 'POST':
        valor = Decimal(request.POST.get('valor'))
        metodo_de_pago = request.POST.get('metodo_de_pago')

        cuenta_por_cobrar = CuentaPorCobrar.objects.get(id=cuenta_id)
        tercero = cuenta_por_cobrar.tercero

        if valor > cuenta_por_cobrar.saldo:
            messages.error(request, "El valor del pago no puede ser mayor al saldo pendiente.")
            return redirect('get_all_cuentas_por_cobrar')

        ingreso = Ingreso(
            fecha=request.POST.get('fecha'),
            tercero=tercero,
            valor=valor,
            creado_por=request.user,
            metodo_de_pago=metodo_de_pago,
            cuenta_por_cobrar=cuenta_por_cobrar
        )

        cuenta_por_cobrar.saldo -= valor

        # Si el saldo llega a 0, cambiar estado a "Pagado"
        if cuenta_por_cobrar.saldo == 0:
            cuenta_por_cobrar.estado = "PAGADO"

        cuenta_por_cobrar.ingresos.add(ingreso)
        cuenta_por_cobrar.save()
        ingreso.save()
        messages.success(request, "Pago registrado correctamente.")
        return redirect('get_all_cuentas_por_cobrar')

    return HttpResponse("Método no permitido", status=405)

def get_all_ingresos(request):
    ingresos = Ingreso.objects.all()

    # Filtro por fecha si se proporciona en la consulta
    fecha_query = request.GET.get('fecha')
    if fecha_query:
        ingresos = ingresos.filter(fecha=fecha_query)

    paginator = Paginator(ingresos, 20)
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual
    context = {'ingresos': page_obj, 'query': fecha_query}

    return render(request, 'ingresos/ingresos.html', context)

@login_required
def delete_ingreso(request, id):
    ingreso = Ingreso.objects.get(id=id)
    if request.method == "POST":
        ingreso.delete()
        messages.success(request, "Ingreso eliminado correctamente.")
        return redirect('get_all_ingresos')
