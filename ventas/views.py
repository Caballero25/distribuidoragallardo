from datetime import date
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cuentasporcobrar.models import CuentaPorCobrar
from ingresos.models import Ingreso
from productos.models import Producto
from terceros.models import Tercero
from ventas.models import Venta, ProductosVendidos
from django.utils.dateparse import parse_date
from django.db import transaction
from .forms import VentaEditForm
from home.models import Parametrizacion

# Create your views here.

@login_required
def get_venta_by_id(request, id):
    if request.method == 'GET':
        venta = Venta.objects.get(id=id)
        context = {'venta': venta}
        return render(request, 'productos/producto.html', context)

@login_required
def get_all_ventas(request):
    ventas = Venta.objects.all().order_by("-fecha", "-fecha_creacion")

    fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    fecha_fin = request.GET.get('fecha_fin', '').strip()
    tercero = request.GET.get('tercero', '').strip()

    if fecha_inicio and fecha_fin:
        fecha_inicio = parse_date(fecha_inicio)
        fecha_fin = parse_date(fecha_fin)
        if fecha_inicio and fecha_fin:
            ventas = ventas.filter(fecha__range=[fecha_inicio, fecha_fin])

    if tercero:
        ventas = ventas.filter(tercero__nombre__icontains=tercero)

    paginator = Paginator(ventas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Si es una solicitud AJAX, devolvemos solo la tabla
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'ventas/ventas_table.html', {'ventas': page_obj})

    return render(request, 'ventas/ventas.html', {'ventas': page_obj})

@login_required
@transaction.atomic
def create_venta(request):
    if request.method == 'POST':
        # Extraer y validar campos obligatorios
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        descripcion = request.POST.get('descripcion')
        valor = float(request.POST.get('valor', 0))  # Valor total de la venta
        cobrado = float(request.POST.get('cobrado', 0))  # Monto cobrado (por defecto 0)
        creado_por = request.user

        if not fecha or not tercero_id or valor <= 0:
            print(fecha)
            print(tercero_id)
            return render(request, 'ventas/create_venta.html', {
                'error': 'Fecha, Tercero y Valor Total son campos obligatorios. El valor total debe ser mayor a 0.',
            })

        try:
            tercero = Tercero.objects.get(id=tercero_id)
        except Tercero.DoesNotExist:
            return render(request, 'ventas/create_venta.html', {
                'error': 'El tercero especificado no existe.',
            })

        # Crear la venta
        venta = Venta(
            fecha=fecha,
            tercero=tercero,
            descripcion=descripcion,
            valor=valor,
            creado_por=creado_por,
        )
        venta.save()

        # Procesar los productos vendidos
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
                # Verificar que el producto exista
                if not producto_id.strip():
                    return render(request, 'ventas/create_venta.html', {
                        'error': f'El producto "{nombre_producto}" no existe. Solo se pueden usar productos existentes.',
                    })

                try:
                    producto = Producto.objects.get(id=producto_id)
                except Producto.DoesNotExist:
                    return render(request, 'ventas/create_venta.html', {
                        'error': f'El producto con ID {producto_id} no existe.',
                    })

                # Crear el registro de producto vendido
                producto_vendido = ProductosVendidos(
                    venta=venta,
                    producto=producto,
                    cantidad=int(cantidad),
                    valor_unitario=float(valor_unitario),
                    valor_total=float(valor_total),
                )
                producto_vendido.save()

                # Actualizar las salidas y la existencia del producto
                producto.salidas += int(cantidad)
                producto.existencia -= int(cantidad)
                producto.save()

        # Calcular el saldo de la cuenta por cobrar
        saldo = valor - cobrado

        # Determinar el estado de la cuenta por cobrar
        estado = 'PAGADO' if saldo <= 0 else 'PENDIENTE'    
        es_credito = True if estado == 'PENDIENTE' else 'False'

        # Crear la cuenta por cobrar asociada a la venta
        cuenta_por_cobrar = CuentaPorCobrar(
            fecha=fecha,
            tercero=tercero,
            venta=venta,
            saldo=saldo,
            estado=estado,
            pertenece_credito=es_credito,
            creado_por=creado_por,
        )
        cuenta_por_cobrar.save()

        # Asignar la cuenta por cobrar a la venta
        venta.cuenta_por_cobrar = cuenta_por_cobrar
        venta.save()  # Guardar la venta con la cuenta por cobrar asignada

        # Crear un ingreso si hay un monto cobrado
        if cobrado > 0:
            metodo_pago = request.POST.get('metodo_pago', 'EFECTIVO')  # Obtener el método de pago del formulario
            ingreso = Ingreso(
                fecha=fecha,
                tercero=tercero,
                valor=cobrado,
                metodo_de_pago=metodo_pago,
                cuenta_por_cobrar=cuenta_por_cobrar,
                pertenece_credito=es_credito,
                creado_por=creado_por,
            )
            ingreso.save()
            cuenta_por_cobrar.ingresos.add(ingreso)
            cuenta_por_cobrar.save()

        messages.success(request, "Venta creada exitosamente.")
        return redirect('get_all_ventas')

    else:
        terceros = Tercero.objects.all()
        productos = Producto.objects.all()

        return render(request, 'ventas/create_venta.html', {
            'terceros': terceros,
            'productos': productos,
        })

@login_required
def delete_venta(request, id):
    try:
        venta = Venta.objects.get(id=id)
    except Venta.DoesNotExist:
        return render(request, 'compras/error.html', {
            'error_message': f"No se encontró la venta con ID {id}."
        })

    if request.method == "POST":
        producto = venta.producto

        # Solo actualizar la existencia del producto si el valor unitario no es cero
        if producto and venta.valor_unitario != Decimal('0'):
            cantidad = venta.valor_total / venta.valor_unitario
            producto.existencia += cantidad
            producto.save()

        # Eliminar la venta en cualquier caso
        venta.delete()
        messages.success(request, "Venta eliminada exitosamente.")
        return redirect('get_all_ventas')

    return render(request, 'ventas/delete_confirm.html', {'venta': venta})

def ventaUpdateView(request, id):
    passwords = Parametrizacion.objects.filter()[0]
    if passwords:
        editar_password = passwords.clave_editar_ventas
    else:
        editar_password = ""
    record = get_object_or_404(Venta, id=id)
    context = {}
    context['title'] = 'Editar Venta'
    context['record'] = record
    if request.method == 'POST':
        form = VentaEditForm(request.POST, instance=record)
        if form.is_valid():
            password = form.cleaned_data.get('password')  
            if password == editar_password:
                form.save()
                return redirect('get_all_ventas')
            else:
                context['error_message'] = "Contraseña incorrecta"
                context['form'] = form
                return render(request, 'ventas/edit.html', context)
        else:
            return render(request, 'ventas/edit.html', context)
    else:
        form = VentaEditForm(instance=record)
    context['form'] = form
    return render(request, 'ventas/edit.html', context)