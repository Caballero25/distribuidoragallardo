from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cuentasporpagar.models import CuentaPorPagar
from .models import Egreso
from django.contrib import messages


@login_required
def get_egreso_by_id(request, id):
    if request.method == 'GET':
        egreso = Egreso.objects.get(id=id)
        context = {'egreso': egreso}
        return render(request, 'productos/producto.html', context)

@login_required
def create_egreso(request, cuenta_id):
    if request.method == 'POST':
        valor = Decimal(request.POST.get('valor'))
        metodo_de_pago = request.POST.get('metodo_de_pago')
        fecha = request.POST.get('fecha')

        cuenta_por_pagar = CuentaPorPagar.objects.get(id=cuenta_id)
        tercero = cuenta_por_pagar.tercero

        if valor > cuenta_por_pagar.saldo:
            messages.error(request, "El valor del pago no puede ser mayor al saldo pendiente.")
            return redirect('get_all_cuentas_por_pagar')

        # Crear y guardar el egreso
        egreso = Egreso(
            fecha=fecha,
            tercero=tercero,
            valor=valor,
            creado_por=request.user,
            metodo_de_pago=metodo_de_pago,
            cuenta_por_pagar=cuenta_por_pagar
        )

        egreso.save()

        cuenta_por_pagar.egresos.add(egreso)

        # Restar el valor del egreso al saldo de la cuenta
        cuenta_por_pagar.saldo -= valor

        # Si el saldo llega a 0, cambiar estado a "Pagado"
        if cuenta_por_pagar.saldo == 0:
            cuenta_por_pagar.estado = "PAGADO"

        # Guardar los cambios en la cuenta por pagar
        cuenta_por_pagar.save()

        messages.success(request, "Pago registrado correctamente.")

        return redirect('get_all_cuentas_por_pagar')

    return HttpResponse("Método no permitido", status=405)

@login_required
def get_all_egresos(request):
    if request.method == 'GET':
        egresos = Egreso.objects.all()
        paginator = Paginator(egresos, 20)
        page_number = request.GET.get('page')  # Obtiene el número de página de la URL
        page_obj = paginator.get_page(page_number)  # Obtiene la página actual
        context = {'egresos': page_obj}
        return render(request, 'egresos/egresos.html', context)

@login_required
def delete_egreso(request, id):
    egreso = Egreso.objects.get(id=id)
    if request.method == "POST":
        egreso.delete()
        messages.success(request, "Egreso eliminado correctamente.")
        return redirect('get_all_egresos')