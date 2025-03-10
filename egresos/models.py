from django.contrib.auth.models import User
from django.db import models
from terceros.models import Tercero

# Create your models here.
class Egreso(models.Model):
    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'EFECTIVO'),
        ('TRANSFERENCIA', 'TRANSFERENCIA')
    ]

    fecha = models.DateField(auto_now=False)
    tercero = models.ForeignKey(Tercero, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    metodo_de_pago = models.CharField(max_length=255, choices=METODO_PAGO_CHOICES)
    cuenta_por_pagar = models.ForeignKey('cuentasporpagar.CuentaPorPagar', on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now=True)
    descripcion = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        nombre_tercero = self.tercero.nombre if self.tercero else "Sin tercero"
        return "$"+str(self.valor) + " " + nombre_tercero + " | " + str(self.fecha)
