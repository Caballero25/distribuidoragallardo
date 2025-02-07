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
        cantidad = int(request.POST.get('cantidad'))
        valor_unitario = Decimal(request.POST.get('valor_unitario'))
        valor_total = cantidad * valor_unitario
        descripcion = request.POST.get('descripcion')

        user = request.user

        producto = Producto.objects.filter(codigo=codigo_producto).first()

        if producto:
            producto.costo_historico += Decimal(str(valor_total))
            producto.existencia += cantidad
            producto.entradas += cantidad
            if producto.entradas > 0:
                producto.costo_unitario = producto.costo_historico / Decimal(producto.entradas)
            producto.save()
        else:
            producto = Producto(
                nombre=nombre_producto,
                codigo=codigo_producto,
                existencia=cantidad,
                valor_unitario=valor_unitario,
                entradas=cantidad,
                salidas=0,
                costo_historico=valor_total,
                costo_unitario=valor_unitario,
                creado_por=user
            )
            producto.save()

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

        messages.success(request, "Compra y cuenta por pagar creadas exitosamente.")
        return redirect('get_all_compras')

    return render(request, 'compras/create_compra.html')

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
        #producto.existencia -= cantidad
        #producto.save()  # Guardamos los cambios en el producto

        compra.delete()

        return redirect('get_all_compras')

    return render(request, 'compras/delete_confirm.html', {'compra': compra})
