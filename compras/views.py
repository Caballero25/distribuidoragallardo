from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date, parse_datetime

from compras.models import ProductosComprados
from egresos.models import Egreso
from terceros.models import Tercero
from .models import Compra
from home.models import Parametrizacion
from productos.models import Producto
from django.contrib import messages
from cuentasporpagar.models import CuentaPorPagar
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db import transaction
from .forms import CompraEditForm

# Create your views here.
@login_required
def get_compra_by_id(request, id):
    if request.method == 'GET':
        compra = Compra.objects.prefetch_related('productos_comprados__producto').get(id=id)
        context = {'compra': compra}
        return render(request, 'compras/compra.html', context)

@login_required
def get_all_compras(request):
    compras = Compra.objects.all().order_by("-fecha", "-fecha_creacion")

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
@transaction.atomic
def create_compra(request):
    if request.method == 'POST':
        # Extraer y validar campos obligatorios
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        descripcion = request.POST.get('descripcion')
        valor = float(request.POST.get('valor', 0))  # Valor total de la compra
        pagado = float(request.POST.get('pagado', 0))  # Monto pagado (por defecto 0)
        creado_por = request.user

        if not fecha or not tercero_id or valor <= 0:
            return render(request, 'compras/create_compra.html', {
                'error': 'Fecha, Tercero y Valor son campos obligatorios. El valor debe ser mayor a 0.',
            })

        try:
            tercero = Tercero.objects.get(id=tercero_id)
        except Tercero.DoesNotExist:
            return render(request, 'compras/create_compra.html', {
                'error': 'El tercero especificado no existe.',
            })

        # Crear la compra
        compra = Compra(
            fecha=fecha,
            tercero=tercero,
            descripcion=descripcion,
            valor=valor,
            creado_por=creado_por,
        )
        compra.save()

        # Procesar los productos comprados
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
                # Si no hay un ID de producto, crear uno nuevo
                if not producto_id.strip():
                    producto, created = Producto.objects.get_or_create(
                        nombre=nombre_producto,
                        codigo=codigo_producto,
                        defaults={
                            'existencia': 0,
                            'valor_unitario': 0,
                            'entradas': 0,
                            'salidas': 0,
                        },
                        creado_por = creado_por
                    )
                else:
                    try:
                        producto = Producto.objects.get(id=producto_id)
                    except Producto.DoesNotExist:
                        return render(request, 'compras/create_compra.html', {
                            'error': f'El producto con ID {producto_id} no existe.',
                        })

                # Crear el registro de producto comprado
                producto_comprado = ProductosComprados(
                    compra=compra,
                    producto=producto,
                    cantidad=int(cantidad),
                    valor_unitario=float(valor_unitario),
                    valor_total=float(valor_total),
                )
                producto_comprado.save()

                # Actualizar las entradas y la existencia del producto
                producto.entradas += int(cantidad)
                producto.existencia += int(cantidad)
                producto.save()

        # Calcular el saldo de la cuenta por pagar
        saldo = valor - pagado

        # Determinar el estado de la cuenta por pagar
        estado = 'PAGADO' if saldo <= 0 else 'PENDIENTE'

        # Crear la cuenta por pagar asociada a la compra
        cuenta_por_pagar = CuentaPorPagar(
            fecha=fecha,
            tercero=tercero,
            compra=compra,
            saldo=saldo,
            estado=estado,
            creado_por=creado_por,
        )
        cuenta_por_pagar.save()

        # Asignar la cuenta por pagar a la compra
        compra.cuenta_por_pagar = cuenta_por_pagar
        compra.save()  # Guardar la compra con la cuenta por pagar asignada

        # Crear un egreso si hay un monto pagado
        if pagado > 0:
            metodo_pago = request.POST.get('metodo_pago', 'EFECTIVO')  # Obtener el método de pago del formulario
            egreso = Egreso(
                fecha=fecha,
                tercero=tercero,
                valor=pagado,
                metodo_de_pago=metodo_pago,
                cuenta_por_pagar=cuenta_por_pagar,
                creado_por=creado_por,
            )
            egreso.save()
            cuenta_por_pagar.egresos.add(egreso)
            cuenta_por_pagar.save()

        messages.success(request, "Compra creada exitosamente.")
        return redirect('get_all_compras')

    else:
        terceros = Tercero.objects.all()
        productos = Producto.objects.all()

        return render(request, 'compras/create_compra.html', {
            'terceros': terceros,
            'productos': productos,
        })

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



def compraUpdateView(request, id):
    passwords = Parametrizacion.objects.filter()[0]
    if passwords:
        editar_password = passwords.clave_editar_compras
    else:
        editar_password = ""
    record = get_object_or_404(Compra, id=id)
    context = {}
    context['title'] = 'Editar Compra'
    context['record'] = record
    if request.method == 'POST':
        form = CompraEditForm(request.POST, instance=record)
        if form.is_valid():
            password = form.cleaned_data.get('password')  
            if password == editar_password:
                form.save()
                return redirect('get_all_compras')
            else:
                context['error_message'] = "Contraseña incorrecta"
                context['form'] = form
                return render(request, 'ventas/edit.html', context)
        else:
            return render(request, 'ventas/edit.html', context)
    else:
        form = CompraEditForm(instance=record)
    context['form'] = form
    return render(request, 'ventas/edit.html', context)