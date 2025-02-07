from django.shortcuts import render, redirect
from .models import Tercero
from .forms import TerceroForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
@login_required
def get_all_terceros(request):
        terceros = Tercero.objects.all()
        context = {'terceros': terceros}
        if request.method == 'GET':
                return render(request, 'terceros/terceros.html', context)

@login_required
def get_tercero_by_id(request, id):
    if request.method == 'GET':
        tercero = Tercero.objects.get(id=id)
        context = {'tercero': tercero}
        return render(request, 'terceros/tercero.html', context)

@login_required
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

@login_required
def create_tercero(request):
        if request.method == 'POST':
                form = TerceroForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect('get_all_terceros')
        else:
                form = TerceroForm()
        return render(request, 'terceros/create_tercero.html', {'form': form})

@login_required
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

@login_required
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

@login_required
def get_tercero_by_name_din(request):
    term = request.GET.get('term', '')
    terceros = Tercero.objects.filter(nombre__icontains=term)[:5]

    data = [{"id": tercero.id, "text": tercero.nombre} for tercero in terceros]
    return JsonResponse(data, safe=False)
        



