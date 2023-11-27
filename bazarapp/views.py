from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto
from .forms import FormProducto


from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')


def vendedor(request):
    return render(request, 'vendedor.html')

from django.shortcuts import render

def jefe_de_ventas(request):
    return render(request, 'jefe_de_ventas/jefe_de_ventas.html')


def read_productos(request):
    productos = Producto.objects.all()
    data = {'productos':productos}
    return render(request, 'jefe_de_ventas/productos/read_productos.html', data)

def add_producto(request):
    form = FormProducto()

    if request.method == "POST":
        form = FormProducto(request.POST)
        if form.is_valid():
            form.save()
            return read_productos(request)

    data = {'form': form,'valor':'Agregar','desc':'Agregue los datos del productos que desea agregar:'}
    return render(request, 'jefe_de_ventas/productos/add_producto.html', data)

def edit_producto(request, id):
    p = Producto.objects.get(id = id)
    form = FormProducto(instance=p)

    if request.method == "POST":
        form = FormProducto(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return read_productos(request)

    data = {'form': form,'valor':'Editar','desc':'Modifique los datos del productos que decia cambiar:'}
    return render(request, 'jefe_de_ventas/productos/add_producto.html', data)

def del_producto(request, id):
    p = Producto.objects.get(id = id)
    p.delete()
    return read_productos(request)

def hacer_venta(request):
    if request.method == 'POST':
        # Obtener el carrito actual de la sesión o crear uno nuevo
        carrito = request.session.get('carrito', [])

        for producto in Producto.objects.all():
            cantidad = request.POST.get(f'cantidad_{producto.id}')
            if cantidad:
                cantidad = int(cantidad)
                if cantidad > 0:
                    # Buscar si el producto ya está en el carrito
                    encontrado = False
                    for item in carrito:
                        if item['producto_id'] == producto.id:
                            item['cantidad'] += cantidad
                            encontrado = True
                            break

                    # Si el producto no está en el carrito, agregarlo
                    if not encontrado:
                        carrito.append({'producto_id': producto.id, 'cantidad': cantidad})

        if carrito:
            # Guardar el carrito en la sesión del usuario
            request.session['carrito'] = carrito
            messages.success(request, 'Productos agregados al carrito.')
            return redirect('carrito')
        else:
            messages.warning(request, 'No se seleccionaron productos.')

    productos = Producto.objects.all()
    return render(request, 'hacer_venta.html', {'productos': productos})


def carrito(request):
    carrito = request.session.get('carrito', [])
    iva = 0
    total = 0
    productos_seleccionados = []

    for item in carrito:
        producto_id = item['producto_id']
        cantidad = item['cantidad']
        try:
            producto = Producto.objects.get(id=producto_id)
            subtotal = producto.precio * cantidad
            iva += (subtotal * 0.12)  # Suponiendo un 12% de IVA
            total += subtotal
            productos_seleccionados.append({'producto': producto, 'cantidad': cantidad})
        except Producto.DoesNotExist:
            messages.warning(request, f'Producto con ID {producto_id} no encontrado.')

    return render(request, 'carrito.html', {
        'carrito': productos_seleccionados,
        'iva': iva,
        'total': total,
    })


def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', [])

    for i, item in enumerate(carrito):
        if item['producto_id'] == producto_id:
            del carrito[i]
            request.session['carrito'] = carrito
            messages.success(request, 'Producto eliminado del carrito exitosamente.')
            return redirect('carrito')

    messages.error(request, 'El producto no estaba en el carrito.')
    return redirect('carrito')

def vaciar_carrito(request):
    request.session['carrito'] = []
    messages.success(request, 'Carrito vaciado exitosamente.')
    return redirect('carrito')



def generar_boleta(request):
    # Lógica para generar boleta
    return HttpResponse("Boleta generada con éxito.")

def generar_factura(request):
    # Lógica para generar factura
    return HttpResponse("Factura generada con éxito.")
