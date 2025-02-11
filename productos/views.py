from django.shortcuts import render, redirect
from django.http import JsonResponse
from productos.forms import ProductoForm
from productos.models import Producto
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def get_all_productos(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    if request.method == 'GET':
        return render(request, 'productos/productos.html', context)

@login_required
def get_producto_by_id(request, id):
    if request.method == 'GET':
        producto = Producto.objects.get(id=id)
        context = {'producto': producto}
        return render(request, 'productos/producto.html', context)

@login_required
def get_producto_by_name(request):
    query = request.GET.get('nombre', '')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()
    form = ProductoForm()
    context = {
        'form': form,
        'productos': productos,
        'query': query
    }
    return render(request, 'productos/productos.html', context)

@login_required
def get_producto_by_name_din(request):
    query = request.GET.get('term', '').strip()  # Cambiar 'q' por 'term'
    productos = Producto.objects.filter(nombre__icontains=query)[:5]  # Limitar a 5 resultados
    data = [{'id': producto.id, 'nombre': producto.nombre} for producto in productos]
    return JsonResponse(data, safe=False)

@login_required
def update_producto(request, id):
    producto = Producto.objects.get(id=id)

    if request.method == 'POST':
        nuevo_valor_unitario = request.POST.get('valor_unitario')

        # Validar que el valor ingresado sea un número válido
        try:
            nuevo_valor_unitario = float(nuevo_valor_unitario)
            if nuevo_valor_unitario <= 0:
                messages.error(request, "El valor unitario debe ser mayor a 0.")
                return redirect('get_all_productos')

            # Actualizar solo el campo valor_unitario
            producto.valor_unitario = nuevo_valor_unitario
            producto.save()

            messages.success(request, "Producto actualizado correctamente.")
        except ValueError:
            messages.error(request, "Ingrese un valor numérico válido.")

        return redirect('get_all_productos')

    return render(request, 'productos/productos.html', {'producto': producto})

@login_required
def delete_producto(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return render(request, 'compras/error.html', {
            'error_message': f"No se encontró la compra con ID {id}."
        })

    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect('get_all_productos')

    return render(request, 'compras/delete_confirm.html', {'producto': producto})

@login_required
def get_codigo_producto(request):
    producto_id = request.GET.get("producto_id")
    if producto_id:
        producto = Producto.objects.filter(id=producto_id).first()
        if producto:
            return JsonResponse({"codigo": producto.codigo})
    return JsonResponse({"codigo": ""})

@login_required
def get_existencia_producto(request):
    producto_id = request.GET.get("producto_id")
    if producto_id:
        producto = Producto.objects.filter(id=producto_id).first()
        if producto:
            return JsonResponse({"existencia": producto.existencia})
    return JsonResponse({"existencia": ""})

@login_required
def get_valor_unitario_producto(request):
    producto_id = request.GET.get("producto_id")
    if producto_id:
        producto = Producto.objects.filter(id=producto_id).first()
        if producto:
            return JsonResponse({"valor_unitario": producto.valor_unitario})
    return JsonResponse({"valor_unitario": ""})
