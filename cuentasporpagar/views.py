from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CuentaPorPagar
from egresos.models import Egreso
from django.http import HttpResponse
from decimal import Decimal

# Create your views here.
def get_all_cuentas_por_pagar(request):
    if request.method == 'GET':
        cuentas_por_pagar = CuentaPorPagar.objects.all()
        context = {'cuentas_por_pagar': cuentas_por_pagar}
        return render(request, 'cuentasporpagar/cuentas_por_pagar.html', context)

def delete_cuenta_por_pagar(request, id):
    cuenta_por_pagar = CuentaPorPagar.objects.get(id=id)
    if request.method == "POST":
        cuenta_por_pagar.delete()
        return redirect('get_all_cuentas_por_pagar')

def create_egreso(request, cuenta_id):
    if request.method == 'POST':
        valor = Decimal(request.POST.get('valor'))
        metodo_de_pago = request.POST.get('metodo_de_pago')

        cuenta_por_pagar = CuentaPorPagar.objects.get(id=cuenta_id)
        tercero = cuenta_por_pagar.tercero

        if valor > cuenta_por_pagar.saldo:
            messages.error(request, "El valor del pago no puede ser mayor al saldo pendiente.")
            return redirect('get_all_cuentas_por_pagar')

        egreso = Egreso(
            fecha=request.POST.get('fecha'),
            tercero=tercero,
            valor=valor,
            creado_por=request.user,
            metodo_de_pago=metodo_de_pago,
            cuenta_por_pagar=cuenta_por_pagar
        )

        cuenta_por_pagar.saldo -= valor

        # Si el saldo llega a 0, cambiar estado a "Pagado"
        if cuenta_por_pagar.saldo == 0:
            cuenta_por_pagar.estado = "Pagado"

        cuenta_por_pagar.save()
        egreso.save()
        messages.success(request, "Pago registrado correctamente.")
        return redirect('get_all_cuentas_por_pagar')

    return HttpResponse("Método no permitido", status=405)
