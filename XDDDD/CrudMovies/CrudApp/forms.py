from django import forms
from .models import Critica

class CriticaForm(forms.ModelForm):
    class Meta:
        model = Critica
        fields = ['nombre_pelicula', 'año_estreno', 'puntuacion', 'sinopsis']
