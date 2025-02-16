from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Venta(models.Model):
    fecha = models.DateField(auto_now=False)
    tercero = models.ForeignKey('terceros.Tercero', on_delete=models.SET_NULL, null=True, blank=True)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    producto = models.ForeignKey('productos.Producto', on_delete=models.SET_NULL, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    cuenta_por_cobrar = models.ForeignKey(
        'cuentasporcobrar.CuentaPorCobrar',
        on_delete=models.SET_NULL,
        related_name='ventas_asociadas',
        null=True,
        blank=True,
        default=None
    )
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='ventas_creadas')
    editado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='ventas_editadas')
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_edicion = models.DateField(auto_now=False, null=True, blank=True)