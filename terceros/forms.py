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

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if Tercero.objects.filter(telefono=telefono).exists():
            raise forms.ValidationError("Este número de teléfono ya está registrado.")
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion').strip().lower()  # Convertir a minúsculas
        if Tercero.objects.filter(direccion__iexact=direccion).exists():
            raise forms.ValidationError("Esta dirección ya está registrada.")
        return self.cleaned_data["direccion"]