from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cuentasporcobrar.models import CuentaPorCobrar

# Create your views here.

@login_required
def get_all_cuentas_por_cobrar(request):
    if request.method == 'GET':
        cuentas_por_cobrar = CuentaPorCobrar.objects.all()
        context = {'cuentas_por_cobrar': cuentas_por_cobrar}
        return render(request, 'cuentasporcobrar/cuentasporcobrar.html', context)

@login_required
def delete_cuenta_por_cobrar(request, id):
    cuenta_por_cobrar = CuentaPorCobrar.objects.get(id=id)
    if request.method == "POST":
        cuenta_por_cobrar.delete()
        return redirect('get_all_cuentas_por_cobrar')