from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=4)
    existencia = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario_credito = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=None)
    entradas = models.IntegerField()
    salidas = models.IntegerField()
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_creados')
    editado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_editados')

    def __str__(self):
        return self.nombre + " | " + "en stock :" + str(self.existencia)
    def save(self, *args, **kwargs):
        if self.valor_unitario_credito is None:
            self.valor_unitario_credito = self.valor_unitario
        super().save(*args, **kwargs)