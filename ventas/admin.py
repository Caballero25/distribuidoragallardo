from django.contrib import admin
from .models import Venta, ProductosVendidos
# Register your models here.

admin.site.register(Venta)
admin.site.register(ProductosVendidos)