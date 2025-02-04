from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo', 'existencia', 'valor_unitario', 'entradas', 'salidas', 'costo_unitario']

class ProductoPrecioForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['valor_unitario']
