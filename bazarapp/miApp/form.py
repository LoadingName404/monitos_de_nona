from django import forms
from miApp.models import Producto, Estante

class FormProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class FormEstante(forms.ModelForm):
    class Meta:
        model = Estante
        fields = '__all__'