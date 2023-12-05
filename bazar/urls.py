
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
    path('vendedor/read_ventas/', views.read_ventas, name='read_ventas'),
    path('vendedor/add_venta/', views.add_venta, name='add_venta'),
    path('vendedor/add_producto_venta/<int:id>', views.add_producto_venta, name='add_producto_venta'),
    path('vendedor/edit_producto_venta/<int:id>', views.edit_producto_venta, name='edit_producto_venta'),
    path('vendedor/add_factura/<int:id>', views.add_factura, name='add_factura'),
]

