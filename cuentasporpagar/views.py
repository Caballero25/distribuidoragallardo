from django.shortcuts import render, redirect
from terceros.models import  Tercero
from django.contrib import messages
from .models import Egreso, CuentaPorPagar
from django.http import HttpResponse
from decimal import Decimal

# Create your views here.
def create_cuenta_por_pagar(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        tercero_id = request.POST.get('tercero')
        compra = request.POST.get('compra')
        saldo = request.POST.get('saldo')
        egresos_id = request.POST.get('egresos')
        usuario = request.POST.get('usuario')
        estado = request.POST.get('estado')

        tercero = Tercero.objects.get(id=tercero_id)

        egreso = Egreso.objects.get(id=egresos_id) if egresos_id else None

        cuenta_por_pagar = CuentaPorPagar(
            fecha=fecha,
            tercero=tercero,
            compra=compra,
            saldo=saldo,
            egresos=egreso,
            usuario=usuario,
            estado=estado
        )

        cuenta_por_pagar.save()

        cuenta_por_pagar_details = {
            'fecha': cuenta_por_pagar.fecha,
            'tercero': cuenta_por_pagar.tercero.nombre,
            'saldo': cuenta_por_pagar.saldo,
            'usuario': cuenta_por_pagar.usuario,
            'estado': cuenta_por_pagar.estado
        }

        return redirect('get_all_cuentas_por_pagar')

    return render(request, 'cuentasporpagar/create_cuenta_por_pagar.html')

def get_all_cuentas_por_pagar(request):
    if request.method == 'GET':
        cuentas_por_pagar = CuentaPorPagar.objects.all()
        context = {'cuentas_por_pagar': cuentas_por_pagar}
        return render(request, 'cuentasporpagar/cuentas_por_pagar.html', context)

def delete_cuenta_por_pagar(request, id):
    cuenta_por_pagar = CuentaPorPagar.objects.get(id=id)
    if request.method == "POST":
        cuenta_por_pagar.delete()
        return redirect('get_all_cuentas_por_pagar')

def create_egreso(request, cuenta_id):
    if request.method == 'POST':
        valor = Decimal(request.POST.get('valor'))
        metodo_de_pago = request.POST.get('metodo_de_pago')
        tercero_id = request.POST.get('tercero')

        cuenta_por_pagar = CuentaPorPagar.objects.get(id=cuenta_id)
        tercero = cuenta_por_pagar.tercero  # Tercero ya está relacionado con la cuenta por pagar

        if valor > cuenta_por_pagar.saldo:
            messages.error(request, "El valor del pago no puede ser mayor al saldo pendiente.")
            return redirect('get_all_cuentas_por_pagar')

        egreso = Egreso(
            fecha=request.POST.get('fecha'),  # Aquí puedes agregar una fecha si es necesario
            tercero=tercero,
            valor=valor,
            usuario=request.user.username,  # O el nombre de usuario del usuario que realiza el pago
            metodo_de_pago=metodo_de_pago,
            cuenta_por_pagar=cuenta_por_pagar
        )

        cuenta_por_pagar.saldo -= valor

        # Si el saldo llega a 0, cambiar estado a "Pagado"
        if cuenta_por_pagar.saldo == 0:
            cuenta_por_pagar.estado = "Pagado"

        cuenta_por_pagar.save()
        egreso.save()
        messages.success(request, "Pago registrado correctamente.")
        return redirect('get_all_cuentas_por_pagar')

    return HttpResponse("Método no permitido", status=405)
