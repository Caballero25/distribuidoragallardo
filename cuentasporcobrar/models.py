from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class CuentaPorCobrar(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'PENDIENTE'),
        ('PAGADO', 'PAGADO')
    ]

    fecha = models.DateField(auto_now=False)
    tercero = models.ForeignKey('terceros.Tercero', on_delete=models.SET_NULL, null=True, blank=True)
    venta = models.ForeignKey(
        'ventas.Venta',
        on_delete=models.CASCADE,
        related_name='cuentas_por_cobrar_relacionadas'
    )
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    ingresos = models.ManyToManyField('ingresos.Ingreso', blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cuentas_por_cobrar')
    estado = models.CharField(max_length=255, choices=ESTADO_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now=True)