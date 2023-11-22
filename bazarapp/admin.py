from django.contrib import admin
from .models import Cargo, Productos, Usuarios, Jornadas, Ventas, Carrito

# Register your models here.

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'sku')

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'nombre_completo', 'id_cargo')

@admin.register(Jornadas)
class JornadasAdmin(admin.ModelAdmin):
    list_display = ('estado', 'fecha_inicio', 'fecha_cierre')

@admin.register(Ventas)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'id_usuario', 'id_jornada')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'id_venta')
