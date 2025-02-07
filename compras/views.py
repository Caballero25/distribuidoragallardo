from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Compra
from productos.models import Producto
from django.contrib import messages
from cuentasporpagar.models import CuentaPorPagar
from terceros.models import Tercero
"""from django.contrib.auth.decorators import login_required"""
# Create your views here.

"""@login_required"""
def get_all_compras(request):
    compras = Compra.objects.all()
    context = {'compras': compras}
    if request.method == 'GET':
        return render(request, 'compras/compras.html', context)

"""@login_required"""
def create_compra(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        producto = request.POST.get('producto')
        valor_unitario = request.POST.get('valor_unitario')
        valor_total = request.POST.get('valor_total')
        descripcion = request.POST.get('descripcion')
        usuario = request.POST.get('usuario')

        # Crear la compra
        compra = Compra.objects.create(
            fecha=fecha,
            tercero_id=tercero_id,
            producto=producto,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            descripcion=descripcion,
            cuenta_por_pagar=cuenta_por_pagar,
            usuario=usuario
        )

        # Crear automáticamente la cuenta por pagar
        cuenta_por_pagar = CuentaPorPagar.objects.create(
            fecha=fecha,
            tercero_id=tercero_id,
            compra=compra,  # Relación con la compra recién creada
            saldo=valor_total,  # Mismo valor que el total de la compra
            usuario=usuario,
            estado='PENDIENTE'
        )

        messages.success(request, "Compra y cuenta por pagar creadas exitosamente.")
        return redirect('lista_compras')  # Redirigir a la lista de compras

    return render(request, 'compras/create_compra.html')

def get_tercero_by_name_din(request):
    if request.method == "GET":
        query = request.GET.get("q", "")
        terceros = Compra.objects.filter(tercero__icontains=query).values_list("tercero", flat=True).distinct()
        return JsonResponse(list(terceros), safe=False)

def get_producto_by_name_din(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query)[:5]  # Limitar a 5 resultados
    data = [{'id': producto.id, 'nombre': producto.nombre} for producto in productos]
    return JsonResponse(data, safe=False)


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
        # Restar la cantidad de las existencias del producto
        #producto.existencia -= cantidad
        #producto.save()  # Guardamos los cambios en el producto

        # Borrar la compra
        compra.delete()

        return redirect('get_all_compras')

    return render(request, 'compras/delete_confirm.html', {'compra': compra})
