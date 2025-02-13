from datetime import date
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from cuentasporcobrar.models import CuentaPorCobrar
from productos.models import Producto
from ventas.models import Venta
from django.utils.dateparse import parse_date

# Create your views here.

@login_required
def get_venta_by_id(request, id):
    if request.method == 'GET':
        venta = Venta.objects.get(id=id)
        context = {'venta': venta}
        return render(request, 'productos/producto.html', context)

@login_required
def get_all_ventas(request):
    ventas = Venta.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()
    tercero = request.GET.get('tercero', '').strip()

    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        if fecha_inicio and fecha_fin:
            ventas = ventas.filter(fecha__range=[fecha_inicio, fecha_fin])

    if tercero:
        ventas = ventas.filter(tercero__nombre__icontains=tercero)

    paginator = Paginator(ventas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Si es una solicitud AJAX, devolvemos solo la tabla
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'ventas/ventas_table.html', {'ventas': page_obj})

    return render(request, 'ventas/ventas.html', {'ventas': page_obj})

@login_required
def create_venta(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad'))
        valor_unitario = Decimal(request.POST.get('valor_unitario'))
        valor_total = cantidad * valor_unitario
        descripcion = request.POST.get('descripcion')
        user = request.user

        producto = Producto.objects.filter(id=producto_id).first()

        if not producto:
            messages.error(request, "El producto seleccionado no existe.")
            return redirect('create_venta')

        if producto.existencia < cantidad:
            messages.error(request, "No hay suficiente existencia para realizar la venta.")
            return redirect('create_venta')

        # Actualizar existencia del producto
        producto.salidas += cantidad
        producto.existencia = producto.entradas - producto.salidas
        producto.save()

        # Crear la venta
        venta = Venta(
            fecha=fecha,
            tercero_id=tercero_id,
            producto=producto,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            descripcion=descripcion,
            creado_por=user
        )
        venta.save()

        # Crear cuenta por cobrar
        cuenta_por_cobrar = CuentaPorCobrar(
            fecha=fecha,
            tercero_id=tercero_id,
            venta=venta,
            saldo=valor_total,
            creado_por=user,
            estado='PENDIENTE'
        )
        cuenta_por_cobrar.save()

        venta.cuenta_por_cobrar = cuenta_por_cobrar
        venta.save()

        messages.success(request, "Venta creada exitosamente.")
        return redirect('get_all_ventas')

    return render(request, 'ventas/create_venta.html')

@login_required
def update_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad'))
        valor_unitario = Decimal(request.POST.get('valor_unitario'))
        valor_total = cantidad * valor_unitario
        descripcion = request.POST.get('descripcion')
        user = request.user

        producto = Producto.objects.filter(id=producto_id).first()

        if not producto:
            messages.error(request, "El producto seleccionado no existe.")
            return redirect('update_venta', venta_id=venta.id)

        # Revertir la salida anterior del producto antes de actualizar
        if venta.producto:
            venta.producto.salidas -= cantidad
            venta.producto.existencia = venta.producto.entradas - venta.producto.salidas
            venta.producto.save()

        # Verificar que haya suficiente stock para la nueva cantidad
        if producto.existencia < cantidad:
            messages.error(request, "No hay suficiente existencia para realizar la venta.")
            return redirect('update_venta', venta_id=venta.id)

        # Actualizar la existencia del producto con los nuevos valores
        producto.salidas += cantidad
        producto.existencia = producto.entradas - producto.salidas
        producto.save()

        # Actualizar la venta
        venta.fecha = fecha
        venta.tercero_id = tercero_id
        venta.producto = producto
        venta.valor_unitario = valor_unitario
        venta.valor_total = valor_total
        venta.descripcion = descripcion
        venta.editado_por = user
        venta.fecha_edicion = date.today()
        venta.save()

        # Actualizar la cuenta por cobrar asociada
        if venta.cuenta_por_cobrar:
            cuenta_por_cobrar = venta.cuenta_por_cobrar
            cuenta_por_cobrar.fecha = fecha
            cuenta_por_cobrar.tercero_id = tercero_id
            cuenta_por_cobrar.saldo = valor_total
            cuenta_por_cobrar.save()

        messages.success(request, "Venta actualizada exitosamente.")
        return redirect('get_all_ventas')

    return render(request, 'ventas/update_venta.html', {'venta': venta})

@login_required
def delete_venta(request, id):
    try:
        venta = Venta.objects.get(id=id)
    except Venta.DoesNotExist:
        return render(request, 'compras/error.html', {
            'error_message': f"No se encontró la venta con ID {id}."
        })

    if request.method == "POST":
        producto = venta.producto

        if producto:  # Validar si la venta tiene un producto asociado
            cantidad = venta.valor_total / venta.valor_unitario
            producto.existencia += cantidad
            producto.save()

        venta.delete()
        return redirect('get_all_ventas')

    return render(request, 'ventas/delete_confirm.html', {'venta': venta})