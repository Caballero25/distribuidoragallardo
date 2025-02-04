from django import forms
from .models import Tercero

class TerceroForm(forms.ModelForm):
    class Meta:
        model = Tercero
        fields = ['nombre', 'tipo', 'telefono', 'direccion']
        widgets = {
            'tipo': forms.Select(choices=Tercero.TipoTercero.choices),
        }