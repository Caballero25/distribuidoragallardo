from decimal import Decimal
from idlelib.rpc import request_queue

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from productos.forms import ProductoForm
from productos.models import Producto
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required
def create_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        codigo = request.POST.get('codigo')
        entradas = int(request.POST.get('entradas', 0))
        salidas = 0  # Se inicializa en 0 porque es un nuevo producto
        existencia = entradas - salidas
        costo_unitario = Decimal(request.POST.get('costo_unitario', 0))
        valor_unitario = Decimal(request.POST.get('valor_unitario', 0))
        creado_por = request.user

        # Validaciones básicas
        if not nombre or not codigo or entradas < 0 or costo_unitario < 0 or valor_unitario < 0:
            messages.error(request, "Los valores ingresados no pueden ser negativos o estar vacíos.")
            return render(request, 'productos/create_producto.html')

        # Verificar si el producto ya existe
        if Producto.objects.filter(codigo=codigo).exists():
            messages.error(request, "El código del producto ya existe.")
            return render(request, 'productos/create_producto.html')

        # Crear el producto
        producto = Producto(
            nombre=nombre,
            codigo=codigo,
            existencia=existencia,
            valor_unitario=valor_unitario,
            entradas=entradas,
            salidas=salidas,
            creado_por=creado_por
        )
        producto.save()

        messages.success(request, "Producto creado exitosamente.")
        return redirect('get_all_productos')

    return render(request, 'productos/create_producto.html')

@login_required
def get_all_productos(request):
    query = request.GET.get('nombre', '')  # Obtiene el nombre si se envió en la búsqueda
    productos = Producto.objects.all()

    if query:
        productos = productos.filter(nombre__icontains=query)

    # Paginación de 20 elementos por página
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual

    context = {
        'productos': page_obj,
        'query': query,
    }
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
        nuevo_nombre = request.POST.get('nombre')
        nuevo_codigo = request.POST.get('codigo')
        nueva_existencia = request.POST.get('existencia')
        editado_por = request.user

        # Validar que el valor ingresado sea un número válido
        try:
            nuevo_valor_unitario = float(nuevo_valor_unitario)
            if nuevo_valor_unitario <= 0:
                messages.error(request, "El valor unitario debe ser mayor a 0.")
                return redirect('get_all_productos')

            # Actualizar solo el campo valor_unitario
            producto.nombre = nuevo_nombre
            producto.codigo = nuevo_codigo
            producto.existencia = nueva_existencia
            producto.valor_unitario = nuevo_valor_unitario
            producto.editado_por = editado_por

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

def validate_nombre(request):
    nombre = request.GET.get('nombre', '').strip()
    existe = Producto.objects.filter(nombre__iexact=nombre).exists()
    return JsonResponse({'existe': existe})

def validate_codigo(request):
    codigo = request.GET.get('codigo', '').strip()
    existe = Producto.objects.filter(codigo__iexact=codigo).exists()
    return JsonResponse({'existe': existe})

def verificar_nombre(request):
    nombre = request.GET.get('nombre')
    producto_id = request.GET.get('id')
    exists = Producto.objects.filter(nombre=nombre).exclude(id=producto_id).exists()
    return JsonResponse({'exists': exists})

def verificar_codigo(request):
    codigo = request.GET.get('codigo')
    producto_id = request.GET.get('id')
    exists = Producto.objects.filter(codigo=codigo).exclude(id=producto_id).exists()
    return JsonResponse({'exists': exists})
