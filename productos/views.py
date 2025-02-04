from django.shortcuts import render, redirect

from productos.forms import ProductoForm
from productos.forms import ProductoPrecioForm
from productos.models import Producto

# Create your views here.
def get_all_productos(request):
    productos = Producto.objects.all()
    context = {'productos': productos}
    if request.method == 'GET':
        return render(request, 'productos/productos.html', context)

def get_producto_by_id(request, id):
    if request.method == 'GET':
        producto = Producto.objects.get(id=id)
        context = {'producto': producto}
        return render(request, 'productos/producto.html', context)

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

def update_producto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('get_all_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/productos.html', {'form': form})

def delete_producto(request, id):
    producto = Producto.objects.get(id=id)
    if request.method == "POST":
        producto.delete()
        return redirect('get_all_productos')
