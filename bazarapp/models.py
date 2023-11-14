from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    sku = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Jornada(models.Model):
    estado = models.BooleanField()
    fecha_inicio = models.DateTimeField()
    fecha_cierre = models.DateTimeField()

    def __str__(self):
        return f"Jornada {self.id}"

class Factura(models.Model):
    razon_social = models.CharField(max_length=200)
    rut = models.CharField(max_length=12)

    def __str__(self):
        return f"Jornada {self.id}"

class Venta(models.Model):
    fecha = models.DateTimeField()
    monto_pagado = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venta {self.id}"

class Carrito(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito {self.id}"
