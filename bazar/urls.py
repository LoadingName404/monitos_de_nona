
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
]
