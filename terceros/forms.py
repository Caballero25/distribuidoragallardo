from django import forms
from .models import Tercero

class TerceroForm(forms.ModelForm):
    telefono = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        widget=forms.TextInput(attrs={'id': 'telefono'}),
        error_messages={
            'required': 'Este campo es obligatorio.',
            'min_length': 'El teléfono debe tener exactamente 10 dígitos.',
            'max_length': 'El teléfono debe tener exactamente 10 dígitos.',
        }
    )

    class Meta:
        model = Tercero
        fields = ['nombre', 'tipo', 'telefono', 'direccion']
        widgets = {
            'tipo': forms.Select(choices=Tercero.TipoTercero.choices),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Tercero.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("Ya existe un tercero con este nombre.")
        return nombre

    