from django.urls import path
from CrudApp import views

urlpatterns = [
    path('', views.lista_criticas, name='lista_criticas'),
    path('agregar/', views.agregar_critica, name='agregar_critica'),
    path('editar/<int:pk>/', views.editar_critica, name='editar_critica'),
    path('eliminar/<int:pk>/', views.eliminar_critica, name='eliminar_critica'),
]