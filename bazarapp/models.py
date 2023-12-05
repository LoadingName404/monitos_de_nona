from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    precio = models.PositiveIntegerField(null=False, blank=False)
    sku = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Jornada(models.Model):
    estado = models.BooleanField(null=False, blank=False)
    fecha_inicio = models.DateTimeField(null=False, blank=False)
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Jornada {self.id}"

class Factura(models.Model):
    razon_social = models.CharField(max_length=200, null=False, blank=False)
    rut = models.CharField(max_length=12, null=False, blank=False)

    def __str__(self):
        return f"Factura {self.razon_social}"

class Venta(models.Model):
    fecha = models.DateTimeField(null=False)
    monto_pagado = models.PositiveIntegerField(null= True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    id_jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE, null=False, blank=False)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Venta {self.id}"

class Carrito(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=False, blank=False)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"Producto {self.id_producto.nombre} de la venta {self.id_venta}"