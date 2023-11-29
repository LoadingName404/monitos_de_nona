
from django.contrib import admin
from django.urls import path
from bazarapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('jefe_de_ventas/', views.jefe_de_ventas, name='jefe_de_ventas'),
    path('jefe_de_ventas/add_productos/', views.add_producto, name='add_productos'),
    path('jefe_de_ventas/read_productos/', views.read_productos, name='read_productos'),
    path('jefe_de_ventas/edit_producto/<int:id>', views.edit_producto),
    path('jefe_de_ventas/del_producto/<int:id>', views.del_producto),
    path('jefe_de_ventas/read_jornadas/', views.read_jornadas),
    path('jefe_de_ventas/abrir_jornada/', views.abrir_jornada),
    path('jefe_de_ventas/cerrar_jornada/', views.cerrar_jornada),

    path('vendedor/', views.vendedor, name='vendedor'),
    path('vendedor/read_productos/', views.only_read_productos, name='only_read_productos'),
    path('vendedor/add_venta/', views.add_venta, name='add_venta'),
    path('vendedor/read_ventas/', views.read_ventas, name='read_ventas'),
    path('vendedor/edit_venta/<int:id>', views.edit_venta),
    path('add_carrito/', views.add_carrito, name='Añadir carrito'),
    path('hacer_venta/', views.hacer_venta, name='hacer_venta'),
    path('carrito/', views.carrito, name='carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('generar_boleta/', views.generar_boleta, name='generar_boleta'),
    path('generar_factura/', views.generar_factura, name='generar_factura'),
]

