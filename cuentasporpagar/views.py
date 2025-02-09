from django.shortcuts import render, redirect
from .models import CuentaPorPagar

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
