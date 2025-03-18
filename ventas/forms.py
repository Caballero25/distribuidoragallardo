from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Venta

class VentaEditForm(forms.ModelForm):
    password = forms.CharField(
            required=True,
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Autorización para editar', 'id': 'id_password'})
        )
    class Meta:
        model = Venta
        fields = ['tercero', 'descripcion']
        widgets = {
            'tercero': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%;',
            }),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción de la venta'}),
        }