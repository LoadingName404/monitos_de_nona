
from django.contrib import admin
from django.urls import path
from bazarapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('jefe_de_ventas/', views.jefe_de_ventas, name='jefe_de_ventas'),
    path('jefe_de_ventas/administracion_productos/', views.administracion_productos, name='administracion_productos'),
    path('jefe_de_ventas/administracion_productos/form_productos/', views.form_productos, name='form_productos'),

    path('vendedor/', views.vendedor, name='vendedor'),
    path('hacer_venta/', views.hacer_venta, name='hacer_venta'),
    path('carrito/', views.carrito, name='carrito'),
]
