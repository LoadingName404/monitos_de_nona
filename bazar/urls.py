
from django.contrib import admin
from django.urls import path
from bazarapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),

    path('jefe_de_ventas/', views.jefe_de_ventas, name='jefe_de_ventas'),
    path('jefe_de_ventas/read_productos/', views.read_productos, name='read_productos'),
    path('jefe_de_ventas/add_productos/', views.add_producto, name='add_productos'),
    path('jefe_de_ventas/edit_producto/<int:id>', views.edit_producto),
    path('jefe_de_ventas/del_producto/<int:id>', views.del_producto),
  
    path('vendedor/', views.vendedor, name='vendedor'),
    path('hacer_venta/', views.hacer_venta, name='hacer_venta'),
    path('carrito/', views.carrito, name='carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('generar_boleta/', views.generar_boleta, name='generar_boleta'),
    path('generar_factura/', views.generar_factura, name='generar_factura'),
]

