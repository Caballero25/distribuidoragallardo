from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import Tercero
from .forms import TerceroForm
from django.http import HttpResponse

# Create your views here.
def get_all_terceros(request):
        terceros = Tercero.objects.all()
        context = {'terceros': terceros}
        if request.method == 'GET':
                return render(request, 'terceros/terceros.html', context)

def get_tercero_by_id(request, id):
    if request.method == 'GET':
        tercero = Tercero.objects.get(id=id)
        context = {'tercero': tercero}
        return render(request, 'terceros/tercero.html', context)

def get_tercero_by_name(request):
    query = request.GET.get('nombre', '')
    if query:
        terceros = Tercero.objects.filter(nombre__icontains=query)
    else:
        terceros = Tercero.objects.all()
    form = TerceroForm()
    context = {
        'form': form,
        'terceros': terceros,
        'query': query
    }
    return render(request, 'terceros/terceros.html', context)

def create_tercero(request):
        if request.method == 'POST':
                form = TerceroForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect('get_all_terceros')
        else:
                form = TerceroForm()
        return render(request, 'terceros/create_tercero.html', {'form': form})

def update_tercero(request, id):
        tercero = Tercero.objects.get(id=id)
        if request.method == 'POST':
                form = TerceroForm(request.POST, instance=tercero)
                if form.is_valid():
                        form.save()
                        return redirect('get_all_terceros')
        else:
                form =TerceroForm(instance=tercero)
        return render(request, 'terceros/terceros.html', {'form': form})

def delete_tercero(request, id):
    try:
        tercero = Tercero.objects.get(id=id)
    except Tercero.DoesNotExist:
        return render(request, 'terceros/error.html', {
            'error_message': f"No se encontró el tercero con ID {id}."
        })

    if request.method == "POST":
        tercero.delete()
        return redirect('get_all_terceros')
        



