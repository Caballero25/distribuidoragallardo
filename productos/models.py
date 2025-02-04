from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=4)
    existencia = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    entradas = models.IntegerField()
    salidas = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)