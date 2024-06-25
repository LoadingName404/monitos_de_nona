from django.db import models

class Estante(models.Model):
    numero = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return str(self.numero)

class Producto(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    precio = models.PositiveIntegerField(blank=False, null=False)
    fecha_vencimiento = models.DateField(blank=False, null=False)
    estante = models.ForeignKey(Estante, on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return self.nombre
    