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



"""class CuentaPorPagar(models.Model):
    fecha = models.DateField()
    tercero = models.ForeignKey(
        Tercero, 
        on_delete=models.CASCADE, 
        related_name="cuentas_por_pagar"
    )
    compra = 
    saldo = models.DecimalField()
    ingreso =
    usuario =
    estado =

class Estado(models.TextChoices):
    PAGADO = "PAGADO", "Pagado"
    PENDIENTE = "PENDIENTE", "Pendiente"

class CuentaPorCobrar(models.Model):
    fecha = models.DateField()
    tercero = models.ForeignKey(
        Tercero, 
        on_delete=models.CASCADE, 
        related_name="cuentas_por_cobrar"
    )
    venta = tercero = models.ForeignKey(
        Venta, 
        on_delete=models.CASCADE, 
        related_name="cuenta_por_cobrar"
    )
    saldo = models.DecimalField()
    ingreso =
    usuario = 
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )


class Venta(models.Model):
    fecha = models.DateField()
    tercero = tercero = models.ForeignKey(
        Tercero, 
        on_delete=models.CASCADE, 
        related_name="ventas"
    )
    producto =
    valor = models.DecimalField(validators=[MinValueValidator(0)])
    descripcion = models.TextField(blank=True, null=True)
    cuenta_por_cobrar = models.OneToOneField(
        CuentaPorCobrar, 
        on_delete=models.SET_NULL, 
        null=False, 
        blank=False,
        related_name="venta"
    )
    usuario = 
    editado_por = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="editado_por"
    )
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_edicion = models.DateField(auto_now_add=True)

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.CharField(
        max_length=255,
        unique=True,
        validators=[EmailValidator(message="Debe ingresar un correo electrónico válido.")]
    )
    contraseña = models.CharField(max_length=255)"""


    