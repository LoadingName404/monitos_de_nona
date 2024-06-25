from django.contrib import admin
from miApp.models import Estante, Producto

# Register your models here.
class EstanteAdmin(admin.ModelAdmin):
    list_display = ['numero']

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'estante', 'precio']

admin.site.register(Estante, EstanteAdmin)
admin.site.register(Producto, ProductoAdmin)