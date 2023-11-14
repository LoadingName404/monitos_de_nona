from django.shortcuts import render, redirect
from bazarapp.models import Producto, Carrito, Venta
from .forms import LoginForm

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def vendedor(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
    else:
        form = LoginForm()

    return render(request, 'vendedor.html', {'form': form})


def jefe_de_ventas(request):
    return render(request, 'jefe_de_ventas/jefe_de_ventas.html')

def administracion_productos(request):
    productos = Producto.objects.all()
    return render(request, 'jefe_de_ventas/productos/administracion_productos.html', {'productos': productos})

def form_productos(request):
    return render(request, 'jefe_de_ventas/productos/form_productos.html')


def hacer_venta(request):
    if request.method == 'POST':
        # Procesar la selección de productos y agregar al carrito
        carrito = []  # Lista para almacenar los productos seleccionados

        for producto in Producto.objects.all():
            cantidad = request.POST.get(f'cantidad_{producto.id}')
            if cantidad:
                cantidad = int(cantidad)
                if cantidad > 0:
                    carrito.append({'producto': producto, 'cantidad': cantidad})

        # Calcular el IVA y el total
        iva = 0
        total = 0

        for item in carrito:
            precio = item['producto'].precio
            cantidad = item['cantidad']
            subtotal = precio * cantidad
            iva += (subtotal * 0.12)  # Suponiendo un 12% de IVA
            total += subtotal

        return render(request, 'carrito.html', {
            'carrito': carrito,
            'iva': iva,
            'total': total,
        })

    productos = Producto.objects.all()
    return render(request, 'hacer_venta.html', {'productos': productos})

# Nueva vista para mostrar el carrito y generar la boleta
def carrito(request):
    # Lógica para mostrar el carrito y generar la boleta
    # Puedes calcular el IVA y el total nuevamente si es necesario
    productos_seleccionados = []  # Agrega aquí los productos seleccionados
    iva = 0  # Calcula el IVA
    total = 0  # Calcula el total

    return render(request, 'carrito.html', {
        'productos_seleccionados': productos_seleccionados,
        'iva': iva,
        'total': total,
    })
