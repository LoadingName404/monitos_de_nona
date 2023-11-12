from django.db import models

class Cargo(models.Model):
    nombre = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre

class Productos(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    sku = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Usuarios(models.Model):
    nombre_usuario = models.CharField(max_length=50)
    nombre_completo = models.CharField(max_length=250)
    contra = models.CharField(max_length=20)
    id_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_usuario

class Jornadas(models.Model):
    estado = models.BooleanField()
    fecha_inicio = models.DateTimeField()
    fecha_cierre = models.DateTimeField()

    def __str__(self):
        return f"Jornada {self.id}"

class Ventas(models.Model):
    fecha = models.DateTimeField()
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    id_jornada = models.ForeignKey(Jornadas, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venta {self.id}"

class Carrito(models.Model):
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito {self.id}"
