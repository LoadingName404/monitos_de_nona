from django.shortcuts import render, redirect
from django.contrib import messages
from miApp.models import Estante, Producto
from miApp.form import FormEstante, FormProducto

# Create your views here.
def index(request):
    estantes = Estante.objects.all()
    data = {'estantes' : estantes}
    return render(request, 'index.html', data)

def estante(request, e_id):
    productos = Producto.objects.filter(estante_id=e_id)
    estante = Estante.objects.get(id=e_id)
    data = {'productos' : productos, 'estante' : estante}
    return render(request, 'estante.html', data)

def create_estante(req):
    form = FormEstante()

    if req.method == "POST":
        try:
            form = FormEstante(req.POST)
            if form.is_valid():
                form.save()
                estante = Estante.objects.last()
                messages.success(req, f'Se agrego el estante {estante.numero} correctamente.')
                return redirect('/')
        except Exception as e:
            messages.error(req, f'No se pudo agregar el estante. Error: {str(e)}')

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue el numero del estante nuevo que desea agregar.'}
    return render(req, 'cu_estante.html', data)


def update_estante(req, e_id):
    estante = Estante.objects.get(id=e_id)
    form = FormEstante(instance=estante)

    if req.method == "POST":
        form = FormEstante(req.POST, instance=estante)
        if form.is_valid():
            try:
                estante.save()
                messages.success(req, f'Se edito el numero del estante {estante.numero} correctamente.')
                return redirect(f'/estante/{e_id}')
            except Exception as e:
                messages.error(req, f'No se pudo cambiar el numero del estante. Error: {str(e)}')

    data = {'form': form, 'accion':'Editar', 'desc':'Cambia el numero del estante al que desea:'}
    return render(req, 'cu_estante.html', data)

def delete_estante(req, e_id):
    estante = Estante.objects.get(id=e_id)
    try:
        estante.delete()
        messages.success(req, f'Se elimino el estante {estante.numero} correctamente.')
    except Exception as e:
        messages.error(req, f'No se pudo eliminar el estante. Error: {str(e)}')
    return redirect('/')

def create_producto(req, e_id):
    form = FormProducto()

    if req.method == "POST":
        try:
            form = FormProducto(req.POST)
            if form.is_valid():
                form.save()
                producto = Producto.objects.last()
                messages.success(req, f'Se agrego el producto {producto.nombre} correctamente.')
                return redirect('/')
        except Exception as e:
            messages.error(req, f'No se pudo agregar el producto. Error: {str(e)}')

    data = {'form': form, 'accion': 'Agregar', 'descripcion': 'Agregue el numero del estante nuevo que desea agregar.'}
    return render(req, 'cu_producto.html', data)

def update_producto(req, p_id):
    producto = Producto.objects.get(id=p_id)
    form = FormProducto(instance=producto)

    if req.method == "POST":
        form = FormProducto(req.POST, instance=producto)
        if form.is_valid():
            try:
                producto.save()
                messages.success(req, f'Se edito el producto {producto.nombre} correctamente.')
                return redirect(f'/estante/{producto.estante}')
            except Exception as e:
                messages.error(req, f'No se pudo editar el producto. Error: {str(e)}')
            

    data = {'form': form, 'accion':'Editar', 'desc':'Modifique los datos del productos que decia cambiar:'}
    return render(req, 'cu_producto.html', data)

def delete_producto(req, p_id):
    producto = Producto.objects.get(id=p_id)
    try:
        producto.delete()
        messages.success(req, f'Se elimino el producto {producto.nombre} correctamente.')
    except Exception as e:
        messages.error(req, f'No se pudo eliminar el producto. Error: {str(e)}')
    return redirect(f'/estante/{producto.estante}')

