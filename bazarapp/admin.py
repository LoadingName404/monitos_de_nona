from django.contrib import admin
from .models import Producto, Jornada, Venta, Carrito, Factura

# Register your models here.

@admin.register(Producto)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'sku')


@admin.register(Jornada)
class JornadasAdmin(admin.ModelAdmin):
    list_display = ('estado', 'fecha_inicio', 'fecha_cierre')

@admin.register(Venta)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'id_jornada', 'id_factura', 'tipo_documento')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'id_venta', 'cantidad_productos')

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('direccion', 'comuna', 'razon_social', 'rut', 'fono')