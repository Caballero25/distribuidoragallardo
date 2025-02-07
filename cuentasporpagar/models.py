from django.db import models
from terceros.models import Tercero
from egresos.models import Egreso

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
        related_name='cuentas_relacionadas'  # Evita conflictos con la relación inversa
    )
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    egresos = models.ForeignKey(
        'egresos.Egreso',
        on_delete=models.SET_NULL,
        null=True, blank=True  # Permite que no siempre tenga un egreso
    )
    usuario = models.CharField(max_length=255)
    estado = models.CharField(max_length=255, choices=ESTADO_CHOICES)