from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CuentaPorPagar
from django.contrib import messages

# Create your views here.

@login_required
def get_cuenta_por_pagar_by_id(request, id):
    if request.method == 'GET':
        cuenta_por_pagar = CuentaPorPagar.objects.get(id=id)
        context = {'cuenta_por_pagar': cuenta_por_pagar}
        return render(request, 'productos/producto.html', context)

@login_required
def get_all_cuentas_por_pagar(request):
    if request.method == 'GET':
        cuentas_por_pagar = CuentaPorPagar.objects.all()
        context = {'cuentas_por_pagar': cuentas_por_pagar}
        return render(request, 'cuentasporpagar/cuentas_por_pagar.html', context)

@login_required
def delete_cuenta_por_pagar(request, id):
    cuenta_por_pagar = CuentaPorPagar.objects.get(id=id)
    if request.method == "POST":
        cuenta_por_pagar.delete()
        messages.success(request, "Cuenta por pagar eliminada correctamente.")
        return redirect('get_all_cuentas_por_pagar')
