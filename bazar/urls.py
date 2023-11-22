
from django.contrib import admin
from django.urls import path
from bazarapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lista_productos/', views.lista_productos, name='lista_productos'),
    path('', views.index),
    path('vendedor/', views.vendedor, name='vendedor'),
    path('jefe_de_ventas/', views.jefe_de_ventas, name='jefe_de_ventas'),
    path('hacer_venta/', views.hacer_venta, name='hacer_venta'),
    path('carrito/', views.carrito, name='carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('generar_boleta/', views.generar_boleta, name='generar_boleta'),
    path('generar_factura/', views.generar_factura, name='generar_factura'),
]

