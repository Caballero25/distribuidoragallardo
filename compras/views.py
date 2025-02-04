from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Compra
from .forms import CompraForm
from productos.models import Producto
from terceros.models import Tercero
"""from django.contrib.auth.decorators import login_required"""
# Create your views here.


"""@login_required"""
def get_all_compras(request):
    compras = Compra.objects.all().select_related('tercero', 'producto', 'cuenta_por_pagar').order_by('-fecha_creacion')
    context = {'compras': compras}
    return render(request, 'compras/compras.html', context)

"""@login_required"""
def create_compra(request):
    if request.method == "POST":
        form = CompraForm(request.POST)
        nuevo_producto = request.POST.get("nuevo_producto", "").strip()

        if form.is_valid():
            compra = form.save(commit=False)
            compra.usuario = request.user

            # Si el usuario ingresa un nuevo producto, créalo
            if not compra.producto and nuevo_producto:
                producto, created = Producto.objects.get_or_create(nombre=nuevo_producto, defaults={'codigo': 'N/A', 'existencia': 0, 'valor_unitario': 0, 'entradas': 0, 'salidas': 0, 'costo_unitario': 0})
                compra.producto = producto

            compra.save()
            return redirect("lista_compras")  # Redirige a la lista de compras

    else:
        form = CompraForm()

    productos = Producto.objects.all()
    terceros = Tercero.objects.all()
    return render(request, "compras/create_compra.html", {"form": form, "productos": productos, "terceros": terceros})

def get_terceros(request):
    if request.GET.get("q"):
        query = request.GET.get("q").strip()
        terceros = Tercero.objects.filter(nombre__icontains=query)[:5]  # Limitar los resultados a 5

        terceros_data = list(terceros.values("id", "nombre"))
        return JsonResponse({
            "terceros": terceros_data,
        })
    return JsonResponse({"terceros": []})

def get_producto(request):
    if request.GET.get("q"):
        query = request.GET.get("q").strip()
        productos = Producto.objects.filter(nombre__icontains=query)

        # Paginación: 5 productos por página
        paginator = Paginator(productos, 5)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        productos_data = list(page_obj.object_list.values("id", "nombre"))
        return JsonResponse({
            "productos": productos_data,
            "has_next": page_obj.has_next(),
        }, safe=False)
    return JsonResponse({"productos": [], "has_next": False}, safe=False)
