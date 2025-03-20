from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.db.models import Sum

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
    context = {}
    cuentas_por_pagar = CuentaPorPagar.objects.all().order_by("-fecha", "-fecha_creacion")

    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()
    tercero = request.GET.get('tercero', '').strip()

    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        if fecha_inicio and fecha_fin:
            cuentas_por_pagar = cuentas_por_pagar.filter(fecha__range=[fecha_inicio, fecha_fin])

    if tercero:
        cuentas_por_pagar = cuentas_por_pagar.filter(tercero__nombre__icontains=tercero)
        saldo_por_tercero = (
            cuentas_por_pagar
            .values('tercero__nombre')
            .annotate(total_saldo=Sum('saldo'))
            .order_by('tercero__nombre')
        )
        if saldo_por_tercero:
            context['saldo_por_tercero'] = saldo_por_tercero

    paginator = Paginator(cuentas_por_pagar, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['cuentas_por_pagar'] = page_obj

    return render(request, 'cuentasporpagar/cuentasporpagar.html', context)

@login_required
def delete_cuenta_por_pagar(request, id):
    cuenta_por_pagar = CuentaPorPagar.objects.get(id=id)
    if request.method == "POST":
        cuenta_por_pagar.delete()
        messages.success(request, "Cuenta por pagar eliminada correctamente.")
        return redirect('get_all_cuentas_por_pagar')
