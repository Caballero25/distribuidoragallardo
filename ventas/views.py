from datetime import date
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from cuentasporcobrar.models import CuentaPorCobrar
from productos.models import Producto
from terceros.models import Tercero
from ventas.models import Venta
from django.utils.dateparse import parse_date
from django.db import transaction

# Create your views here.

@login_required
def get_venta_by_id(request, id):
    if request.method == 'GET':
        venta = Venta.objects.get(id=id)
        context = {'venta': venta}
        return render(request, 'productos/producto.html', context)

@login_required
def get_all_ventas(request):
    ventas = Venta.objects.all().order_by("-fecha", "-fecha_creacion")

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
@transaction.atomic
def create_venta(request):
    if request.method == 'POST':
        # Extraer y validar campos obligatorios
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        descripcion = request.POST.get('descripcion')
        valor_total = float(request.POST.get('valor_total', 0))  # Valor total de la venta
        cobrado = float(request.POST.get('cobrado', 0))  # Monto cobrado (por defecto 0)
        creado_por = request.user

        if not fecha or not tercero_id or valor_total <= 0:
            return render(request, 'ventas/create_venta.html', {
                'error': 'Fecha, Tercero y Valor Total son campos obligatorios. El valor total debe ser mayor a 0.',
            })

        try:
            tercero = Tercero.objects.get(id=tercero_id)
        except Tercero.DoesNotExist:
            return render(request, 'ventas/create_venta.html', {
                'error': 'El tercero especificado no existe.',
            })

        # Crear la venta
        venta = Venta(
            fecha=fecha,
            tercero=tercero,
            descripcion=descripcion,
            valor_total=valor_total,
            creado_por=creado_por,
        )
        venta.save()

        # Procesar los productos vendidos
        productos_ids = request.POST.getlist('producto[]')
        nombres_productos = request.POST.getlist('producto_nombre[]')
        codigos_productos = request.POST.getlist('producto_codigo[]')
        cantidades = request.POST.getlist('cantidad[]')
        valores_unitarios = request.POST.getlist('valor_unitario[]')
        valores_totales = request.POST.getlist('valor_total[]')

        for producto_id, nombre_producto, codigo_producto, cantidad, valor_unitario, valor_total in zip(productos_ids,
                                                                                                        nombres_productos,
                                                                                                        codigos_productos,
                                                                                                        cantidades,
                                                                                                        valores_unitarios,
                                                                                                        valores_totales):
            if nombre_producto.strip() and codigo_producto.strip() and cantidad.strip() and valor_unitario.strip() and valor_total.strip():
                # Verificar que el producto exista
                if not producto_id.strip():
                    return render(request, 'ventas/create_venta.html', {
                        'error': f'El producto "{nombre_producto}" no existe. Solo se pueden usar productos existentes.',
                    })

                try:
                    producto = Producto.objects.get(id=producto_id)
                except Producto.DoesNotExist:
                    return render(request, 'ventas/create_venta.html', {
                        'error': f'El producto con ID {producto_id} no existe.',
                    })

                # Crear el registro de producto vendido
                producto_vendido = ProductosVendidos(
                    venta=venta,
                    producto=producto,
                    cantidad=int(cantidad),
                    valor_unitario=float(valor_unitario),
                    valor_total=float(valor_total),
                )
                producto_vendido.save()

                # Actualizar las salidas y la existencia del producto
                producto.salidas += int(cantidad)
                producto.existencia -= int(cantidad)
                producto.save()

        # Calcular el saldo de la cuenta por cobrar
        saldo = valor_total - cobrado

        # Determinar el estado de la cuenta por cobrar
        estado = 'PAGADO' if saldo <= 0 else 'PENDIENTE'

        # Crear la cuenta por cobrar asociada a la venta
        cuenta_por_cobrar = CuentaPorCobrar(
            fecha=fecha,
            tercero=tercero,
            venta=venta,
            saldo=saldo,
            estado=estado,
            creado_por=creado_por,
        )
        cuenta_por_cobrar.save()

        # Asignar la cuenta por cobrar a la venta
        venta.cuenta_por_cobrar = cuenta_por_cobrar
        venta.save()  # Guardar la venta con la cuenta por cobrar asignada

        # Crear un ingreso si hay un monto cobrado
        if cobrado > 0:
            metodo_pago = request.POST.get('metodo_pago', 'EFECTIVO')  # Obtener el método de pago del formulario
            ingreso = Ingreso(
                fecha=fecha,
                tercero=tercero,
                valor=cobrado,
                metodo_de_pago=metodo_pago,
                cuenta_por_cobrar=cuenta_por_cobrar,
                creado_por=creado_por,
            )
            ingreso.save()
            cuenta_por_cobrar.ingresos.add(ingreso)
            cuenta_por_cobrar.save()

        messages.success(request, "Venta creada exitosamente.")
        return redirect('get_all_ventas')

    else:
        terceros = Tercero.objects.all()
        productos = Producto.objects.all()

        return render(request, 'ventas/create_venta.html', {
            'terceros': terceros,
            'productos': productos,
        })

@login_required
def update_venta(request, venta_id):
    venta = Venta.objects.get(id=venta_id)

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

        # Solo actualizar la existencia del producto si el valor unitario no es cero
        if producto and venta.valor_unitario != Decimal('0'):
            cantidad = venta.valor_total / venta.valor_unitario
            producto.existencia += cantidad
            producto.save()

        # Eliminar la venta en cualquier caso
        venta.delete()
        messages.success(request, "Venta eliminada exitosamente.")
        return redirect('get_all_ventas')

    return render(request, 'ventas/delete_confirm.html', {'venta': venta})