from django.shortcuts import render, redirect
from .models import Egreso


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