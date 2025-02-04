from django import forms
from .models import Compra


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['tercero', 'producto', 'valor_unitario', 'valor_total', 'descripcion', 'cuenta_por_pagar']

        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }