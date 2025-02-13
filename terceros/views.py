from django.shortcuts import render, redirect
from .models import Tercero
from .forms import TerceroForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def validate_tercero(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        direccion = request.POST.get("direccion", "").strip().lower()  # Ignorar mayúsculas/minúsculas

        if nombre and Tercero.objects.filter(nombre__iexact=nombre).exists():
            return JsonResponse({"error": "Ya existe un tercero con este nombre."})

        if telefono and Tercero.objects.filter(telefono=telefono).exists():
            return JsonResponse({"error": "Ya existe un tercero con este teléfono."})

        if direccion and Tercero.objects.filter(direccion__iexact=direccion).exists():
            return JsonResponse({"error": "Ya existe un tercero con esta dirección."})

    return JsonResponse({"error": None})

@login_required
def get_all_terceros(request):
    query = request.GET.get('nombre', '')  # Obtiene el nombre si se envió en la búsqueda
    terceros = Tercero.objects.all()

    if query:
        terceros = terceros.filter(nombre__icontains=query)

    # Paginación de 20 elementos por página
    paginator = Paginator(terceros, 20)
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página actual

    context = {
        'terceros': page_obj,
        'query': query,
    }
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
            messages.success(request, "Tercero creado exitosamente")
            return JsonResponse({'success': True, 'redirect_url': '/terceros/'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
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
        return render(request, 'compras/error.html', {
            'error_message': f"No se encontró la compra con ID {id}."
        })

    if request.method == "POST":
        tercero.delete()
        messages.success(request, "Tercero eliminado correctamente.")
        return redirect('get_all_terceros')

    return render(request, 'compras/delete_confirm.html', {'tercero': tercero})

@login_required
def get_tercero_by_name_din(request):
    term = request.GET.get('term', '')
    terceros = Tercero.objects.filter(nombre__icontains=term)[:5]

    data = [{"id": tercero.id, "text": tercero.nombre} for tercero in terceros]
    return JsonResponse(data, safe=False)
        



