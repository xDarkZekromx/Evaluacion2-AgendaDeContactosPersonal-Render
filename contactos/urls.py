from django.urls import path
from . import views

urlpatterns = [
    path('personas/', views.lista_contactos, name='lista_contactos'),                   # Pagina de Contactos
    path('personas/nuevo/', views.nuevo_contacto, name='nuevo_contacto'),               # Pagina para agregar nuevo contacto
    path('personas/<int:pk>/', views.detalle_contacto, name='detalle_contacto'),        # Pagina de detalle de contacto
    path('personas/<int:pk>/editar/', views.editar_contacto, name='editar_contacto'),   # Pagina para editar contacto
    path('personas/<int:pk>/eliminar/', views.eliminar_contacto, name='eliminar_contacto'),     # Pagina para eliminar contacto
    
]