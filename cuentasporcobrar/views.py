from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.db.models import Sum
from decimal import Decimal
from django.shortcuts import get_object_or_404

from cuentasporcobrar.models import CuentaPorCobrar
from terceros.models import Tercero
from ingresos.models import Ingreso
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
    context = {}
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
        saldo_por_tercero = (
            cuentas_por_cobrar
            .values('tercero__id','tercero__nombre')
            .annotate(total_saldo=Sum('saldo'))
            .order_by('tercero__nombre')
        )
        if saldo_por_tercero:
            context['saldo_por_tercero'] = saldo_por_tercero




    paginator = Paginator(cuentas_por_cobrar, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['cuentas_por_cobrar'] = page_obj

    return render(request, 'cuentasporcobrar/cuentasporcobrar.html', context)

@login_required
def delete_cuenta_por_cobrar(request, id):
    cuenta_por_cobrar = CuentaPorCobrar.objects.get(id=id)
    if request.method == "POST":
        cuenta_por_cobrar.delete()
        messages.success(request, "Cuenta por cobrar eliminada correctamente.")
        return redirect('get_all_cuentas_por_cobrar')
    

def pagoMasivoCuentaPorCobrar(request, id):
    if request.method == 'POST':
        try:
            # Clean data pay
            valor_adeudado = request.POST.get('valor_adeudado', '0')
            valor_adeudado = valor_adeudado.strip().replace(',', '.')
            valor_adeudado = Decimal(valor_adeudado)

            valor_pagado = request.POST.get('valor', '0')
            valor_pagado = valor_pagado.strip().replace(',', '.')
            valor_pagado = Decimal(valor_pagado)
            
            fecha = request.POST.get('fecha')
            metodo_de_pago = request.POST.get('metodo_de_pago')
            descripcion = request.POST.get('descripcion', '')

            tercero = get_object_or_404(Tercero, id=id)

            if valor_pagado <= 0:
                messages.error(request, "El valor del pago debe ser mayor a cero.")
                return redirect('get_all_cuentas_por_cobrar')

            if valor_pagado > valor_adeudado:
                messages.error(request, "El valor del pago no puede ser mayor al saldo pendiente.")
                return redirect('get_all_cuentas_por_cobrar')
            
            cuentas_por_cobrar = CuentaPorCobrar.objects.filter(
                tercero=tercero, 
                estado='PENDIENTE'
            ).order_by('fecha_creacion')

            monto_restante = valor_pagado

            for cuenta in cuentas_por_cobrar:
                if monto_restante <= 0:
                    break
                
                monto_a_aplicar = min(cuenta.saldo, monto_restante)
                
                # Crear el ingreso correspondiente
                ingreso = Ingreso.objects.create(
                    fecha=fecha,
                    tercero=tercero,
                    valor=monto_a_aplicar,
                    creado_por=request.user,
                    metodo_de_pago=metodo_de_pago,
                    cuenta_por_cobrar=cuenta,
                    pertenece_credito=cuenta.pertenece_credito,
                    descripcion=descripcion
                )
                
                # Actualizar la cuenta por cobrar
                cuenta.saldo -= monto_a_aplicar
                cuenta.ingresos.add(ingreso)
                cuenta.save()  # El save() ya actualiza el estado si saldo llega a 0
                
                monto_restante -= monto_a_aplicar

            messages.success(request, f"Pago aplicado correctamente. Monto restante no aplicado: {monto_restante}")
            return redirect('get_all_cuentas_por_cobrar')

        except Exception as e:
            messages.error(request, f"Error al procesar el pago: {str(e)}")
            return redirect('get_all_cuentas_por_cobrar')