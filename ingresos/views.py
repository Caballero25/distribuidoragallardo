from decimal import Decimal
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date

from cuentasporcobrar.models import CuentaPorCobrar
from .models import Ingreso
from django.http import HttpResponse

@login_required
def get_ingreso_by_id(request, id):
    if request.method == 'GET':
        ingreso = Ingreso.objects.get(id=id)
        context = {'ingreso': ingreso}
        return render(request, 'ingresos/ingreso.html', context)

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
        ingreso.save()
        cuenta_por_cobrar.ingresos.add(ingreso)
        cuenta_por_cobrar.save()
        messages.success(request, "Pago registrado correctamente.")
        return redirect('get_all_cuentas_por_cobrar')

    return HttpResponse("Método no permitido", status=405)

@login_required
def get_all_ingresos(request):
    ingresos = Ingreso.objects.all().order_by("-fecha", "-fecha_creacion")

    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()
    tercero = request.GET.get('tercero', '').strip()

    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        if fecha_inicio and fecha_fin:
            ingresos = ingresos.filter(fecha__range=[fecha_inicio, fecha_fin])

    if tercero:
        ingresos = ingresos.filter(tercero__nombre__icontains=tercero)

    paginator = Paginator(ingresos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Si es una solicitud AJAX, devolvemos solo la tabla
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'ingresos/ingresos_table.html', {'ingresos': page_obj})

    return render(request, 'ingresos/ingresos.html', {'ingresos': page_obj})

@login_required
def delete_ingreso(request, id):
    ingreso = Ingreso.objects.get(id=id)
    if request.method == "POST":
        ingreso.delete()
        messages.success(request, "Ingreso eliminado correctamente.")
        return redirect('get_all_ingresos')
