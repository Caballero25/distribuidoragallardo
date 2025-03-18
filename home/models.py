from django.db import models

# Create your models here.

class Parametrizacion(models.Model):
    clave_editar_ventas = models.CharField(max_length=50)
    clave_editar_compras = models.CharField(max_length=50)