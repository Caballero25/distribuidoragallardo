from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from cuentasporcobrar.models import CuentaPorCobrar
from productos.models import Producto
from ventas.models import Venta

# Create your views here.
@login_required
def get_all_ventas(request):
    ventas = Venta.objects.all()
    context = {'ventas': ventas}
    if request.method == 'GET':
        return render(request, 'ventas/ventas.html', context)

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

        messages.success(request, "Venta y cuenta por cobrar creadas exitosamente.")
        return redirect('get_all_ventas')

    return render(request, 'ventas/create_venta.html')


@login_required
def delete_venta(request, id):
    try:
        venta = Venta.objects.get(id=id)
        producto = venta.producto
        cantidad = venta.valor_total / venta.valor_unitario  # Calculamos la cantidad, suponiendo que valor_total = cantidad * valor_unitario
    except Venta.DoesNotExist:
        return render(request, 'compras/error.html', {
            'error_message': f"No se encontró la venta con ID {id}."
        })

    if request.method == "POST":
        producto.existencia += cantidad
        producto.save()

        venta.delete()

        return redirect('get_all_ventas')

    return render(request, 'ventas/delete_confirm.html', {'venta': venta})