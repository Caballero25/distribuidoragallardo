from django.contrib.auth.models import User
from django.db import models

class Compra(models.Model):
    fecha = models.DateField(auto_now=False)
    tercero = models.ForeignKey('terceros.Tercero', on_delete=models.CASCADE)
    producto = models.ForeignKey('productos.Producto', on_delete=models.SET_NULL, null=True, blank=True)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    cuenta_por_pagar = models.ForeignKey(
        'cuentasporpagar.CuentaPorPagar',
        on_delete=models.CASCADE,
        related_name='compras_asociadas',
        null=True,
        blank=True,
        default=None
    )
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
