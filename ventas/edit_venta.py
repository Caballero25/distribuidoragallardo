from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from .models import Venta, ProductosVendidos
from cuentasporcobrar.models import CuentaPorCobrar
from ingresos.models import Ingreso


@login_required
def editar_venta_completa(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    cuenta_por_cobrar = venta.cuenta_por_cobrar
    
    # Verificar permisos o si la venta pertenece al usuario, si es necesario
    
    if request.method == 'POST':
        with transaction.atomic():
            # Procesar cambios en productos vendidos
            print(request.POST)
            if 'update_products' in request.POST:
                productos_ids = request.POST.getlist('producto_id')
                cantidades = request.POST.getlist('cantidad')
                precios_unitarios = request.POST.getlist('valor_unitario')
                
                # Calcular diferencia total en productos
                diferencia_total_productos = Decimal('0')
                
                for i in range(len(productos_ids)):
                    producto_vendido = get_object_or_404(ProductosVendidos, id=productos_ids[i], venta=venta)
                    #Actualizar inventario
                    producto_vendido.producto.existencia += producto_vendido.cantidad 
                    producto_vendido.producto.existencia -= int(cantidades[i])
                    producto_vendido.producto.salidas -= producto_vendido.cantidad
                    producto_vendido.producto.salidas += int(cantidades[i])
                    producto_vendido.producto.save()
                    # Calcular valor total anterior
                    valor_anterior = producto_vendido.valor_total
                    print(producto_vendido.producto.existencia)
                    
                    # Actualizar valores
                    producto_vendido.cantidad = int(cantidades[i])
                    p_unitario = precios_unitarios[i].strip().replace(',', '.')
                    producto_vendido.valor_unitario = Decimal(p_unitario)
                    producto_vendido.valor_total = producto_vendido.cantidad * producto_vendido.valor_unitario
                    producto_vendido.save()
                    
                    # Calcular diferencia
                    diferencia = producto_vendido.valor_total - valor_anterior
                    diferencia_total_productos += diferencia
                
                # Actualizar saldo en cuenta por cobrar
                if cuenta_por_cobrar:
                    cuenta_por_cobrar.saldo += diferencia_total_productos
                    cuenta_por_cobrar.save()
                
                messages.success(request, 'Productos actualizados correctamente')
            
            # Procesar eliminación de productos
            elif 'delete_product' in request.POST:
                print("Delete product #######################################################################")
                producto_id = request.POST.get('delete_product_id')
                producto_vendido = get_object_or_404(ProductosVendidos, id=producto_id, venta=venta)
                
                if cuenta_por_cobrar:
                    cuenta_por_cobrar.saldo -= producto_vendido.valor_total
                    cuenta_por_cobrar.save()
                producto_vendido.producto.existencia += producto_vendido.cantidad
                producto_vendido.producto.salidas -= producto_vendido.cantidad
                producto_vendido.producto.save()
                producto_vendido.delete()
                messages.success(request, 'Producto eliminado de la venta')
            
            # Procesar cambios en ingresos
            elif 'update_ingresos' in request.POST:
                ingresos_ids = request.POST.getlist('ingreso_id')
                valores = request.POST.getlist('valor')
                print(request.POST)
                diferencia_total_ingresos = Decimal('0')
                
                for i in range(len(ingresos_ids)):
                    ingreso = get_object_or_404(Ingreso, id=ingresos_ids[i], cuenta_por_cobrar=cuenta_por_cobrar)
                    ingreso_val = valores[i].strip().replace(',', '.')
                    ingreso_val = Decimal(ingreso_val)
                    # Calcular diferencia
                    
                    diferencia = ingreso_val - ingreso.valor
                    
                    diferencia_total_ingresos += diferencia
                    
                    # Actualizar ingreso
                    ingreso.valor = ingreso_val
                    ingreso.save()
                
                # Actualizar saldo en cuenta por cobrar (restamos porque si el ingreso aumenta, el saldo debe disminuir)
                if cuenta_por_cobrar:
                    cuenta_por_cobrar.saldo -= diferencia_total_ingresos
                    
                    # Verificar si el saldo llegó a cero para marcar como pagado
                    if cuenta_por_cobrar.saldo <= 0:
                        cuenta_por_cobrar.estado = 'PAGADO'
                        #cuenta_por_cobrar.saldo = Decimal('0')  # Evitar saldos negativos
                    else:
                        cuenta_por_cobrar.estado = 'PENDIENTE'
                    
                    cuenta_por_cobrar.save()
                
                messages.success(request, 'Ingresos actualizados correctamente')
            
            # Actualizar datos básicos de la venta si es necesario
            venta.valor = sum(pv.valor_total for pv in venta.productos_vendidos.all())
            venta.save()
            
            return redirect('editar_venta_completa', venta_id=venta.id)
    
    # Obtener todos los productos vendidos e ingresos relacionados
    productos_vendidos = venta.productos_vendidos.all().select_related('producto')
    
    if cuenta_por_cobrar:
        ingresos = cuenta_por_cobrar.ingresos.all()
    else:
        ingresos = []
    
    context = {
        'venta': venta,
        'productos_vendidos': productos_vendidos,
        'ingresos': ingresos,
        'cuenta_por_cobrar': cuenta_por_cobrar,
    }
    
    return render(request, 'ventas/editar_venta_completa.html', context)