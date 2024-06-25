from django.contrib import admin
from django.urls import path
from miApp import views

urlpatterns = [
    path('admin/',                       admin.site.urls),
    path('',                             views.index,           name='index'),
    path('estante/<int:e_id>/',          views.estante,         name='estante'),
    path('agregar_estante',              views.create_estante,  name='create_estante'),
    path('editar_estante/<int:e_id>',    views.update_estante,  name='update_estante'),
    path('eliminar_estante/<int:e_id>',  views.delete_estante,  name='delete_estante'),
    path('agregar_producto/<int:e_id>',  views.create_producto, name='create_producto'),
    path('editar_producto/<int:p_id>',   views.update_producto, name='update_producto'),
    path('eliminar_producto/<int:p_id>', views.delete_producto, name='delete_producto'),
]
