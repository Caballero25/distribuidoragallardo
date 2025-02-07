from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class CuentaPorPagar(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'PENDIENTE'),
        ('PAGADO', 'PAGADO')
    ]

    fecha = models.DateField(auto_now=False)
    tercero = models.ForeignKey('terceros.Tercero', on_delete=models.CASCADE)
    compra = models.ForeignKey(
        'compras.Compra',
        on_delete=models.CASCADE,
        related_name='cuentas_relacionadas'
    )
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    egresos = models.ForeignKey(
        'egresos.Egreso',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=255, choices=ESTADO_CHOICES)