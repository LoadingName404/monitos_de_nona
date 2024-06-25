from django.shortcuts import render, redirect, get_object_or_404
from .models import Critica
from .forms import CriticaForm

def lista_criticas(request):
    criticas = Critica.objects.all()
    return render(request, 'lista_criticas.html', {'criticas': criticas})

def agregar_critica(request):
    if request.method == 'POST':
        form = CriticaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_criticas')
    else:
        form = CriticaForm()
    return render(request, 'agregar_critica.html', {'form': form})

def editar_critica(request, pk):
    critica = get_object_or_404(Critica, pk=pk)
    if request.method == 'POST':
        form = CriticaForm(request.POST, instance=critica)
        if form.is_valid():
            form.save()
            return redirect('lista_criticas')
    else:
        form = CriticaForm(instance=critica)
    return render(request, 'editar_critica.html', {'form': form})

def eliminar_critica(request, pk):
    critica = get_object_or_404(Critica, pk=pk)
    if request.method == 'POST':
        critica.delete()
        return redirect('lista_criticas')
    return render(request, 'confirmar_eliminar.html', {'critica': critica})
