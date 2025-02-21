from django.contrib.auth.models import User
from django.db import models

class Compra(models.Model):
    fecha = models.DateField(auto_now=False)
    tercero = models.ForeignKey('terceros.Tercero', on_delete=models.SET_NULL, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    descripcion = models.TextField(blank=True, null=True)
    cuenta_por_pagar = models.ForeignKey(
        'cuentasporpagar.CuentaPorPagar',
        on_delete=models.CASCADE,
        related_name='compras_asociadas',
        null=True,
        blank=True,
        default=None
    )
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras_creadas')
    fecha_creacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Compra: " + self.creado_por.username +" a " + self.tercero.nombre +" "+ "$"+str(self.valor) + " | " + str(self.fecha)
 
class ProductosComprados(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, related_name='productos_comprados')
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return " cantidad - " +str(self.cantidad) + " | "+self.producto.nombre + " | " +str(self.compra.fecha)