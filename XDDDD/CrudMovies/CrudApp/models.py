from django.db import models

from django.db import models

class Critica(models.Model):
    nombre_pelicula = models.CharField(max_length=200)
    año_estreno = models.IntegerField()
    puntuacion = models.FloatField()
    sinopsis = models.TextField()

    def __str__(self):
        return self.nombre_pelicula