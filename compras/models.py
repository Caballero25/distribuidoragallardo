from django.db import models

from cuentasporpagar.models import CuentaPorPagar
from productos.models import Producto
from terceros.models import Tercero

# Create your models here.
class Compra(models.Model):
    fecha = models.DateField(auto_now=False)
    tercero = models.ForeignKey('terceros.Tercero', on_delete=models.CASCADE)
    producto = models.CharField(max_length=255)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    cuenta_por_pagar = models.ForeignKey(
        'cuentasporpagar.CuentaPorPagar',
        on_delete=models.CASCADE,
        related_name='compras_asociadas'  # Evita conflicto con el campo `compra` en `CuentaPorPagar`
    )
    usuario = models.CharField(max_length=255)
