from django.db import models
from productos.models import Producto
from terceros.models import Tercero

# Create your models here.
class CuentaPorPagar(models.Model):
    id = models.AutoField(primary_key=True)

class User(models.Model):
    id = models.AutoField(primary_key=True)

class Compra(models.Model):
    fecha = models.DateField()
    tercero = models.ForeignKey(Tercero, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField()
    cuenta_por_pagar = models.ForeignKey(CuentaPorPagar, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="compras_creadas")
    editado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="compras_editadas")
    fecha_edicion = models.DateTimeField(auto_now=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
