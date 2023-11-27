from django import forms
from bazarapp.models import Producto

class FormProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'