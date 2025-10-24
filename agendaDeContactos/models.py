from django.db import models 
from django.core.validators import RegexValidator   #Importa validador de numeros


class Contacto(models.Model): 
    nombre = models.CharField(max_length=100)   #Nombre con maximo 100 caracteres
    telefono = models.CharField(    
        max_length=9,
        validators=[
            RegexValidator(                     #Validador de numeros
                regex=r'^[29]\d{8}$',           #Recuadro solicita comenzar con 2 o 9 y tener 9 digitos
                message="El número debe comenzar con 2 (casa) o 9 (móvil) y tener 9 dígitos."   #Mensaje de error    
            )
        ]
    )
    correo = models.EmailField()                #Validador de Emails
    direccion = models.CharField(max_length=200)    #Direccion con maximo 200 caracteres

    def __str__(self):      
        return self.nombre
