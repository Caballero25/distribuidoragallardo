from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from cuentasporcobrar.models import CuentaPorCobrar
from django.contrib import messages

# Create your views here.

@login_required
def get_all_cuentas_por_cobrar(request):
    if request.method == 'GET':
        cuentas_por_cobrar = CuentaPorCobrar.objects.all()
        paginator = Paginator(cuentas_por_cobrar, 20)
        page_number = request.GET.get('page')  # Obtiene el número de página de la URL
        page_obj = paginator.get_page(page_number)  # Obtiene la página actual
        context = {'cuentas_por_cobrar': page_obj}
        return render(request, 'cuentasporcobrar/cuentasporcobrar.html', context)

@login_required
def delete_cuenta_por_cobrar(request, id):
    cuenta_por_cobrar = CuentaPorCobrar.objects.get(id=id)
    if request.method == "POST":
        cuenta_por_cobrar.delete()
        messages.success(request, "Cuenta por cobrar eliminada correctamente.")
        return redirect('get_all_cuentas_por_cobrar')