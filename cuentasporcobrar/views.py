from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from cuentasporcobrar.models import CuentaPorCobrar
from django.contrib import messages

# Create your views here.

@login_required
def get_cuenta_por_cobrar_by_id(request, id):
    if request.method == 'GET':
        cuenta_por_cobrar = CuentaPorCobrar.objects.get(id=id)
        context = {'cuenta_por_cobrar': cuenta_por_cobrar}
        return render(request, 'cuentasporcobrar/cuentaporcobrar.html', context)

@login_required
def get_all_cuentas_por_cobrar(request):
    cuentas_por_cobrar = CuentaPorCobrar.objects.all().order_by("-fecha", "-fecha_creacion")

    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()
    tercero = request.GET.get('tercero', '').strip()

    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        if fecha_inicio and fecha_fin:
            cuentas_por_cobrar = cuentas_por_cobrar.filter(fecha__range=[fecha_inicio, fecha_fin])

    if tercero:
        cuentas_por_cobrar = cuentas_por_cobrar.filter(tercero__nombre__icontains=tercero)

    paginator = Paginator(cuentas_por_cobrar, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Si es una solicitud AJAX, devolvemos solo la tabla
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'cuentas_por_cobrar/cuentas_por_cobrar_table.html', {'cuentas_por_cobrar': page_obj})

    return render(request, 'cuentasporcobrar/cuentasporcobrar.html', {'cuentas_por_cobrar': page_obj})

@login_required
def delete_cuenta_por_cobrar(request, id):
    cuenta_por_cobrar = CuentaPorCobrar.objects.get(id=id)
    if request.method == "POST":
        cuenta_por_cobrar.delete()
        messages.success(request, "Cuenta por cobrar eliminada correctamente.")
        return redirect('get_all_cuentas_por_cobrar')