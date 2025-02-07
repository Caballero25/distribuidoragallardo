from django.shortcuts import render, redirect
from .models import Egreso
from terceros.models import Tercero
from django.http import JsonResponse

# Create your views here.
def get_all_egresos(request):
    if request.method == 'GET':
        egresos = Egreso.objects.all()
        context = {'egresos': egresos}
        return render(request, 'egresos/egresos.html', context)

def delete_egreso(request, id):
    egreso = Egreso.objects.get(id=id)
    if request.method == "POST":
        egreso.delete()
        return redirect('get_all_egresos')

def get_tercero_by_name_din(request):
    term = request.GET.get('term', '')
    terceros = Tercero.objects.filter(nombre__icontains=term)[:5]

    data = [{"id": tercero.id, "text": tercero.nombre} for tercero in terceros]
    return JsonResponse(data, safe=False)