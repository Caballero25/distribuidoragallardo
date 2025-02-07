from django.db import models
from django.core.validators import RegexValidator


class Tercero(models.Model):
    class TipoTercero(models.TextChoices):
        CLIENTE = "CLIENTE", "Cliente"
        PROVEEDOR = "PROVEEDOR", "Proveedor"
        CLIENTE_PROVEEDOR = "CLIENTE/PROVEEDOR", "Cliente/Proveedor"

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=20,
        choices=TipoTercero.choices,
        default=TipoTercero.CLIENTE
    )
    telefono = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="El número de teléfono debe contener 10 dígitos.",
                code='invalid_phone_number'
            )
        ],
        unique=True
    )
    direccion = models.CharField(max_length=100)