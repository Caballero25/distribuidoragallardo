from django.shortcuts import render, redirect
from .models import Compra
from productos.models import Producto
from django.contrib import messages
from cuentasporpagar.models import CuentaPorPagar
from django.contrib.auth.decorators import login_required
from decimal import Decimal

# Create your views here.

@login_required
def get_all_compras(request):
    compras = Compra.objects.all()
    context = {'compras': compras}
    if request.method == 'GET':
        return render(request, 'compras/compras.html', context)

@login_required
def create_compra(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        nombre_producto = request.POST.get('producto_nombre')
        codigo_producto = request.POST.get('producto_codigo')

        cantidad = request.POST.get('cantidad')
        valor_unitario = request.POST.get('valor_unitario')
        valor_total = request.POST.get('valor_total')  # Obtener el valor total desde el formulario

        # Manejo de valores nulos o vacíos
        cantidad = Decimal(cantidad) if cantidad else Decimal(0)
        valor_unitario = Decimal(valor_unitario) if valor_unitario else Decimal(0)
        valor_total = Decimal(valor_total) if valor_total else cantidad * valor_unitario  # Prioriza el valor enviado

        descripcion = request.POST.get('descripcion')
        user = request.user

        # Buscar o crear el producto
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
def delete_compra(request, id):
    try:
        compra = Compra.objects.get(id=id)
        producto = compra.producto  # Obtenemos el producto relacionado con la compra
        cantidad = compra.valor_total / compra.valor_unitario  # Calculamos la cantidad, suponiendo que valor_total = cantidad * valor_unitario
    except Compra.DoesNotExist:
        return render(request, 'compras/error.html', {
            'error_message': f"No se encontró la compra con ID {id}."
        })

    if request.method == "POST":
        producto.existencia -= cantidad
        producto.save() 

        compra.delete()
        messages.success(request, "Compra eliminada correctamente.")
        return redirect('get_all_compras')

    return render(request, 'compras/delete_confirm.html', {'compra': compra})
