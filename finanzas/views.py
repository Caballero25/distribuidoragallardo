from django.shortcuts import render
from ingresos.models import Ingreso
from egresos.models import Egreso
from django.http import JsonResponse

# Create your views here.

def ingresos(request):
    if request.method == "GET":
        return render(request, "finanzas/ingresos.html")
    elif request.method == "POST":
        status = False 
        message = ""
        fecha = request.POST.get('fecha')
        valor = request.POST.get('valor')
        tipo_transaccion = request.POST.get('tipo_transaccion')
        descripcion = request.POST.get('descripcion')
        try:
            nuevo_ingreso = Ingreso()
            nuevo_ingreso.fecha = fecha
            nuevo_ingreso.valor = valor
            nuevo_ingreso.metodo_de_pago = tipo_transaccion
            nuevo_ingreso.descripcion = descripcion
            nuevo_ingreso.save()
            status = True
            message = "Ingreso registrado correctamente"
        except Exception as e:
            message = f"Error al registrar el ingreso: {e}"
        response = JsonResponse({"status": status, "message": message})
        return response


def egresos(request):
    if request.method == "GET":
        return render(request, "finanzas/egresos.html")
    elif request.method == "POST":
        status = False 
        message = ""
        status = False 
        message = ""
        fecha = request.POST.get('fecha')
        valor = request.POST.get('valor')
        tipo_transaccion = request.POST.get('tipo_transaccion')
        descripcion = request.POST.get('descripcion')
        try:
            nuevo_egreso = Egreso()
            nuevo_egreso.fecha = fecha
            nuevo_egreso.valor = valor
            nuevo_egreso.metodo_de_pago = tipo_transaccion
            nuevo_egreso.descripcion = descripcion
            nuevo_egreso.save()
            status = True
            message = "Egreso registrado correctamente"
        except Exception as e:
            message = f"Error al registrar el egreso: {e}"
        response = JsonResponse({"status": status, "message": message})
        return response