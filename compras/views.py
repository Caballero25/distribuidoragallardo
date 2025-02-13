from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from .models import Compra
from productos.models import Producto
from django.contrib import messages
from cuentasporpagar.models import CuentaPorPagar
from django.contrib.auth.decorators import login_required
from decimal import Decimal

# Create your views here.
@login_required
def get_compra_by_id(request, id):
    if request.method == 'GET':
        compra = Compra.objects.get(id=id)
        context = {'compra': compra}
        return render(request, 'compras/compra.html', context)

@login_required
def get_all_compras(request):
    compras = Compra.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()
    tercero = request.GET.get('tercero', '').strip()

    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        if fecha_inicio and fecha_fin:
            compras = compras.filter(fecha__range=[fecha_inicio, fecha_fin])

    if tercero:
        compras = compras.filter(tercero__nombre__icontains=tercero)

    paginator = Paginator(compras, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Si es una solicitud AJAX, devolvemos solo la tabla
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'ventas/ventas_table.html', {'compras': page_obj})

    return render(request, 'compras/compras.html', {'compras': page_obj})

@login_required
def create_compra(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        nombre_producto = request.POST.get('producto_nombre', '').strip()
        codigo_producto = request.POST.get('producto_codigo', '').strip()

        cantidad = request.POST.get('cantidad')
        valor_unitario = request.POST.get('valor_unitario')
        valor_total = request.POST.get('valor_total')  # Puede venir vacío

        # Asegurar que los valores sean numéricos o asignarles 0
        cantidad = Decimal(cantidad) if cantidad and cantidad.isnumeric() else Decimal(0)
        valor_unitario = Decimal(valor_unitario) if valor_unitario and valor_unitario.strip() else Decimal(0)
        valor_total = Decimal(valor_total) if valor_total and valor_total.isnumeric() else cantidad * valor_unitario

        descripcion = request.POST.get('descripcion')
        user = request.user

        # Si no se envía producto ni código, asignar valores específicos
        if not nombre_producto and not codigo_producto:
            cantidad = Decimal(0)
            valor_unitario = Decimal(0)
            # Mantener el valor total enviado en el formulario
            valor_total = Decimal(request.POST.get('valor_total', 0))

        producto = None
        if codigo_producto:
            producto = Producto.objects.filter(codigo=codigo_producto).first()
            if producto:
                producto.costo_historico += valor_total
                producto.existencia += cantidad
                producto.entradas += cantidad
                if producto.entradas > 0:
                    producto.costo_unitario = producto.costo_historico / producto.entradas
                producto.save()
            else:
                producto = Producto(
                    nombre=nombre_producto,
                    codigo=codigo_producto,
                    existencia=cantidad,
                    valor_unitario=0,
                    entradas=cantidad,
                    salidas=0,
                    costo_historico=valor_total,
                    costo_unitario=valor_unitario,
                    creado_por=user
                )
                producto.save()

        # Crear la compra
        compra = Compra(
            fecha=fecha,
            tercero_id=tercero_id,
            producto=producto,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            descripcion=descripcion,
            creado_por=user
        )
        compra.save()

        # Crear la cuenta por pagar
        cuenta_por_pagar = CuentaPorPagar(
            fecha=fecha,
            tercero_id=tercero_id,
            compra=compra,
            saldo=valor_total,
            creado_por=user,
            estado='PENDIENTE'
        )
        cuenta_por_pagar.save()

        compra.cuenta_por_pagar = cuenta_por_pagar
        compra.save()

        messages.success(request, "Compra creada exitosamente.")
        return redirect('get_all_compras')

    return render(request, 'compras/create_compra.html')


@login_required
def update_compra(request, id):
    compra = Compra.objects.get(id=id)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        nombre_producto = request.POST.get('producto_nombre')
        codigo_producto = request.POST.get('producto_codigo')

        cantidad = request.POST.get('cantidad')
        valor_unitario = request.POST.get('valor_unitario')
        valor_total = request.POST.get('valor_total')

        cantidad = Decimal(cantidad) if cantidad else Decimal(0)
        valor_unitario = Decimal(valor_unitario) if valor_unitario else Decimal(0)
        valor_total = Decimal(valor_total) if valor_total else cantidad * valor_unitario

        descripcion = request.POST.get('descripcion')
        user = request.user

        # Buscar o crear el producto
        producto = Producto.objects.filter(codigo=codigo_producto).first()
        if producto:
            # Revertir los valores del producto antes de actualizar
            producto.costo_historico -= compra.valor_total
            producto.existencia -= compra.producto.entradas if compra.producto else 0
            producto.entradas -= compra.producto.entradas if compra.producto else 0

            # Aplicar los nuevos valores
            producto.costo_historico += valor_total
            producto.existencia += cantidad
            producto.entradas += cantidad
            if producto.entradas > 0:
                producto.costo_unitario = producto.costo_historico / producto.entradas
            producto.save()
        else:
            producto = Producto(
                nombre=nombre_producto,
                codigo=codigo_producto,
                existencia=cantidad,
                valor_unitario=0,
                entradas=cantidad,
                salidas=0,
                costo_historico=valor_total,
                costo_unitario=valor_unitario,
                creado_por=user
            )
            producto.save()

        # Actualizar la compra
        compra.fecha = fecha
        compra.tercero_id = tercero_id
        compra.producto = producto
        compra.valor_unitario = valor_unitario
        compra.valor_total = valor_total
        compra.descripcion = descripcion
        compra.editado_por = user
        compra.fecha_edicion = date.today()
        compra.save()

        # Actualizar la cuenta por pagar asociada
        if compra.cuenta_por_pagar:
            cuenta_por_pagar = compra.cuenta_por_pagar
            cuenta_por_pagar.fecha = fecha
            cuenta_por_pagar.tercero_id = tercero_id
            cuenta_por_pagar.saldo = valor_total
            cuenta_por_pagar.save()

        messages.success(request, "Compra actualizada exitosamente.")
        return redirect('get_all_compras')

    return render(request, 'compras/update_compra.html', {'compra': compra})

@login_required
def delete_compra(request, id):
    try:
        compra = Compra.objects.get(id=id)
    except Compra.DoesNotExist:
        return render(request, 'compras/error.html', {
            'error_message': f"No se encontró la compra con ID {id}."
        })

    if request.method == "POST":
        producto = compra.producto

        if producto:  # Validar si la compra tiene un producto asociado
            cantidad = compra.valor_total / compra.valor_unitario if compra.valor_unitario else 0
            producto.existencia -= cantidad
            producto.save()

        compra.delete()
        messages.success(request, "Compra eliminada correctamente.")
        return redirect('get_all_compras')

    return render(request, 'compras/delete_confirm.html', {'compra': compra})
