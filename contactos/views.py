from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Contacto
from .form import ContactoForm

# Create your views here.

#Vista para listar contactos con barra de busqueda
def lista_contactos(request):
    query = request.GET.get("q")
    if query:
        contactos = Contacto.objects.filter(
            Q(nombre__icontains=query) | Q(correo__icontains=query)
        )
    else:
        contactos = Contacto.objects.all()

    return render(request, 'personas/lista_contactos.html', {'contactos': contactos})

#Vista para ver detalle de contacto
def detalle_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    return render(request, 'personas/detalle_contacto.html', {'contacto': contacto})

#Vista para agregar, editar y eliminar contactos
def nuevo_contacto(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm()
    return render(request, 'personas/nuevo_contacto.html', {'form': form})

#Vista para editar contacto
def editar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == "POST":
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'personas/editar_contactos.html', {'form': form})

#Vista para eliminar contacto
def eliminar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == "POST":
        contacto.delete()
        return redirect('lista_contactos')
    return render(request, 'personas/eliminar_contactos.html', {'contacto': contacto})

