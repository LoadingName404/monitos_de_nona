from django import forms
from bazarapp.models import Producto, Carrito, Venta, Factura

class FormProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

class FormCarrito(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = '__all__'

class FormVenta(forms.ModelForm):
    class Meta:
        model = Venta
        fields = '__all__'

class FormFactura(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'