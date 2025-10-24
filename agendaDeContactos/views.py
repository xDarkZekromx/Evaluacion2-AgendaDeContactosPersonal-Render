from django.http import HttpResponse 
from django.shortcuts import render
from contactos.models import Contacto
from django.db.models import Q

#Pagina de inicio

def inicio(request): 
    nombre = "Marcelo Hermosilla"
    return HttpResponse(f"¡Bienvenidos a mi primera agenda en Django, {nombre}!") 


#Intento de vista para listar contactos con barra de busqueda

def lista_contactos(request):
    query = request.GET.get("q")
    if query:
        contactos = Contacto.objects.filter(
            Q(nombre__icontains=query) | Q(correo__icontains=query)
        )
    else:
        contactos = Contacto.objects.all()

    return render(request, "agenda/lista.html", {"contactos": contactos, query: query})

