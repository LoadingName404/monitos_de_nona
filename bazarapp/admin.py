from django.contrib import admin
from .models import Producto, Jornada, Venta, Carrito

# Register your models here.

@admin.register(Producto)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'sku')


@admin.register(Jornada)
class JornadasAdmin(admin.ModelAdmin):
    list_display = ('estado', 'fecha_inicio', 'fecha_cierre')

@admin.register(Venta)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'id_jornada')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'id_venta')
