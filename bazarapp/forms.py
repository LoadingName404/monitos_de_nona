from django import forms
from bazarapp.models import Producto, Carrito
from django.contrib.auth.models import User

class FormProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class FormCarrito(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = '__all__'