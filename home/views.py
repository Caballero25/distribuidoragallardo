from django.shortcuts import render
from django.db import models
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from compras.models import Compra
from ventas.models import Venta
from django.utils.timezone import now, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from productos.models import Producto
# Create your views here.
@login_required
def home(request):
    productos_escasos = Producto.objects.all().order_by('existencia')[:5]
    cantidad_total_productos = Producto.objects.aggregate(total_existencia=models.Sum('existencia'))['total_existencia'] or 0
    total_inventario = Producto.objects.aggregate(total_valor=models.Sum(models.F('existencia') * models.F('valor_unitario')))['total_valor'] or 0

    context = {
        "productos_escasos": productos_escasos,
        "cantidad_total_productos": cantidad_total_productos,
        "total_inventario": total_inventario
    }

    return render(request, 'home/home.html',context)
    

def obtener_ventas(request):
    opcion = request.GET.get('opcion', '7dias')
    hoy = now().date()
    
    if opcion == '7dias':
        fecha_inicio = hoy - timedelta(days=6)
        ventas = Venta.objects.filter(fecha__gte=fecha_inicio)
        ventas = ventas.annotate(periodo=TruncDay('fecha')).values('periodo').annotate(total=Count('id')).order_by('periodo')
    elif opcion == '4semanas':
        fecha_inicio = hoy - timedelta(weeks=4)
        ventas = Venta.objects.filter(fecha__gte=fecha_inicio)
        ventas = ventas.annotate(periodo=TruncWeek('fecha')).values('periodo').annotate(total=Count('id')).order_by('periodo')
    elif opcion == '4meses':
        fecha_inicio = hoy - timedelta(days=4*30)
        ventas = Venta.objects.filter(fecha__gte=fecha_inicio)
        ventas = ventas.annotate(periodo=TruncMonth('fecha')).values('periodo').annotate(total=Count('id')).order_by('periodo')
    else:
        return JsonResponse({'error': 'Opción no válida'}, status=400)
    
    data = {
        'labels': [str(item['periodo']) for item in ventas],
        'values': [item['total'] for item in ventas]
    }
    return JsonResponse(data)

def obtener_compras(request):
    opcion = request.GET.get('opcion', '7dias')
    hoy = now().date()
    
    if opcion == '7dias':
        fecha_inicio = hoy - timedelta(days=6)
        compras = Compra.objects.filter(fecha__gte=fecha_inicio)
        compras = compras.annotate(periodo=TruncDay('fecha')).values('periodo').annotate(total=Count('id')).order_by('periodo')
    elif opcion == '4semanas':
        fecha_inicio = hoy - timedelta(weeks=4)
        compras = Compra.objects.filter(fecha__gte=fecha_inicio)
        compras = compras.annotate(periodo=TruncWeek('fecha')).values('periodo').annotate(total=Count('id')).order_by('periodo')
    elif opcion == '4meses':
        fecha_inicio = hoy - timedelta(days=4*30)
        compras = Compra.objects.filter(fecha__gte=fecha_inicio)
        compras = compras.annotate(periodo=TruncMonth('fecha')).values('periodo').annotate(total=Count('id')).order_by('periodo')
    else:
        return JsonResponse({'error': 'Opción no válida'}, status=400)
    
    data = {
        'labels': [str(item['periodo']) for item in compras],
        'values': [item['total'] for item in compras]
    }
    return JsonResponse(data)