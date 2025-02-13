from datetime import timedelta, date, datetime
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.dateparse import parse_date

from egresos.models import Egreso
from ingresos.models import Ingreso


# Create your views here.
@login_required
def balance(request):
    # Obtener mes y año del parámetro GET o usar el mes y año actuales por defecto
    mes = int(request.GET.get('mes', date.today().month))
    anio = int(request.GET.get('anio', date.today().year))

    # Filtrar ingresos y egresos para el mes seleccionado
    ingresos = Ingreso.objects.filter(fecha__year=anio, fecha__month=mes)
    egresos = Egreso.objects.filter(fecha__year=anio, fecha__month=mes)

    # Convertir ingresos y egresos a un solo formato
    ingresos_list = [
        {'fecha': i.fecha, 'tercero': i.tercero, 'valor': i.valor, 'metodo_de_pago': i.metodo_de_pago, 'tipo': 'Ingreso'}
        for i in ingresos
    ]

    egresos_list = [
        {'fecha': e.fecha, 'tercero': e.tercero, 'valor': e.valor, 'metodo_de_pago': e.metodo_de_pago, 'tipo': 'Egreso'}
        for e in egresos
    ]

    # Combinar y ordenar por fecha descendente
    movimientos = sorted(chain(ingresos_list, egresos_list), key=lambda x: x['fecha'], reverse=True)

    # Calcular totales
    total_ingresos = sum(i['valor'] for i in ingresos_list)
    total_egresos = sum(e['valor'] for e in egresos_list)
    balance_neto = total_ingresos - total_egresos

    # Mapeo de meses en español
    meses_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    meses = [(num, nombre) for num, nombre in meses_es.items()]  # Lista de tuplas [(1, "Enero"), ...]
    anio_actual = datetime.now().year
    anios = list(range(2025, anio_actual + 1))
    context = {
        'movimientos': movimientos,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'balance_neto': balance_neto,
        'mes': mes,
        'anio': anio,
        'meses': meses,
        'anios': anios,
        'nombre_mes_actual': meses_es[mes]
    }
    return render(request, 'balance/balance.html', context)