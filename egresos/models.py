from django.db import models
from terceros.models import Tercero

# Create your models here.
class Egreso(models.Model):
    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'EFECTIVO'),
        ('TRANSFERENCIA', 'TRANSFERENCIA')
    ]

    fecha = models.DateField(auto_now=False)
    tercero = models.ForeignKey(Tercero, on_delete=models.CASCADE)  # Cambio a ForeignKey
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.CharField(max_length=255)
    metodo_de_pago = models.CharField(max_length=255, choices=METODO_PAGO_CHOICES)
    cuenta_por_pagar = models.ForeignKey('cuentasporpagar.CuentaPorPagar', on_delete=models.CASCADE)
