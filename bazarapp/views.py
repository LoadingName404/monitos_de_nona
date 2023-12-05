from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.utils import timezone
from .models import Producto, Venta, Jornada, Carrito, Factura
from .forms import FormProducto, FormFactura

######################## para comprobar si es jefe de ventas o vendedor ################################
#                                                                                                      #
def es_jefe_de_ventas(user):
    return user.groups.filter(name='Jefe de ventas').exists()

def es_vendedor(user):
    return user.groups.filter(name='Vendedor').exists()
#                                                                                                      #
########################################################################################################

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='Jefe de ventas').exists():
                    return redirect('jefe_de_ventas/')
                elif user.groups.filter(name='Vendedor').exists():
                    return redirect('vendedor/')
                else:
                    return HttpResponse('El usuario ingresado no es ni jefe de ventas ni a vendedor, contactar con administrador')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})

################################# Jefe de ventas #################################
#                                                                                #
@user_passes_test(es_jefe_de_ventas)
def jefe_de_ventas(request):
    return render(request, 'jefe_de_ventas/jefe_de_ventas.html')

@user_passes_test(es_jefe_de_ventas)
def read_productos(request):
    productos = Producto.objects.all()
    data = {'productos':productos}
    return render(request, 'jefe_de_ventas/productos/read_productos.html', data)

@user_passes_test(es_jefe_de_ventas)
def add_producto(request):
    form = FormProducto()

    if request.method == "POST":
        form = FormProducto(request.POST)
        if form.is_valid():
            form.save()
            return read_productos(request)

    data = {'form': form,'valor':'Agregar','desc':'Agregue los datos del productos que desea agregar:'}
    return render(request, 'jefe_de_ventas/productos/add_producto.html', data)

@user_passes_test(es_jefe_de_ventas)
def edit_producto(request, id):
    p = Producto.objects.get(id = id)
    form = FormProducto(instance=p)

    if request.method == "POST":
        form = FormProducto(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return read_productos(request)

    data = {'form': form,
            'valor':'Editar',
            'desc':'Modifique los datos del productos que decia cambiar:'}
    return render(request, 'jefe_de_ventas/productos/add_producto.html', data)

@user_passes_test(es_jefe_de_ventas)
def del_producto(request, id):
    p = Producto.objects.get(id = id)
    p.delete()
    return read_productos(request)

@user_passes_test(es_jefe_de_ventas)
def read_jornadas(request):
    jornadas = Jornada.objects.all()
    hay_jornada_abierta = Jornada.objects.filter(estado=True)
    data = {'jornadas':jornadas, 'hay_jornada_abierta':hay_jornada_abierta}
    return render(request, 'jefe_de_ventas/jornadas/read_jornadas.html', data)

@user_passes_test(es_jefe_de_ventas)
def abrir_jornada(request):
    jornada_abierta = Jornada.objects.filter(estado=True).first()
    if not jornada_abierta:
        Jornada.objects.create(estado=True, fecha_inicio=timezone.now())
    return read_jornadas(request)

@user_passes_test(es_jefe_de_ventas)

def cerrar_jornada(request):
    jornada_abierta = Jornada.objects.filter(estado=True).first()
    if jornada_abierta:
        jornada_abierta.estado = False
        jornada_abierta.fecha_cierre = timezone.now()
        jornada_abierta.save()
    return read_jornadas(request)
#                                                                                #
##################################################################################

################################# Vendedor #################################
#                                                                          #
@user_passes_test(es_vendedor)
def vendedor(request):
    return render(request, 'vendedor/vendedor.html')

def only_read_productos(request):
    productos = Producto.objects.all()
    data = {'productos':productos}
    return render(request, 'vendedor/read_productos.html', data)

@user_passes_test(es_vendedor)
def read_ventas(request):
    jornada_abierta = Jornada.objects.filter(estado=True).first()
    if not jornada_abierta:
        return render(request, 'vendedor/ventas/jornada_estado_false.html')
    else:
        ventas = Venta.objects.filter(id_jornada=Jornada.objects.filter(estado=True).first())
        data = {'ventas':ventas}
        return render(request, 'vendedor/ventas/read_ventas.html', data)

@user_passes_test(es_vendedor)
def add_venta(request):
    try:
        Venta.objects.create(fecha=timezone.now(), 
                             id_jornada=Jornada.objects.filter(estado=True).first(), 
                             usuario=request.user)
        id_venta = Venta.objects.last().id
        return redirect(f'/vendedor/add_producto_venta/{id_venta}')
    except:
        return render(request, 'vendedor/ventas/jornada_estado_false.html')
    

@user_passes_test(es_vendedor)
def add_producto_venta(request, id):
    venta = Venta.objects.get(id=id)
    productos = Producto.objects.all()
    if request.method == 'POST':
        for p in productos:
            cantidad = request.POST.get(f'cantidad_{p.id}')
            if cantidad == '':
                cantidad = 0
            for _ in range(int(cantidad)):
                print(f'Se esta agregando el producto {p.nombre}, {cantidad} veces, a la venta {venta.id}')
                Carrito.objects.create(id_producto=p, id_venta=venta)
        monto_pagado = sum([carrito.id_producto.precio for carrito in Carrito.objects.filter(id_venta=venta)])
        venta.monto_pagado = monto_pagado
        venta.save()
        factura = request.POST.get('factura')
        print(factura)
        if factura is not None:
            return redirect(f'/vendedor/add_factura/{id}')
        else:
            return redirect('read_ventas')
    else:
        data = {'venta':venta, 'productos':productos}
        return render(request, 'vendedor/ventas/add_producto_venta.html', data)
    
def add_factura(request, id):
    venta = Venta.objects.get(id=id)
    form = FormFactura()

    if request.method == "POST":
        form = FormFactura(request.POST)
        if form.is_valid():
            factura = form.save() 
            venta.id_factura = factura
            venta.save()
            
            return read_ventas(request)

    data = {'form': form}
    return render(request, 'vendedor/ventas/factura.html', data)
    
@user_passes_test(es_vendedor)
def edit_producto_venta(request, id):
    venta = Venta.objects.get(id=id)
    productos = Producto.objects.all()
    if request.method == 'POST':
        for p in productos:
            cantidad = request.POST.get(f'cantidad_{p.id}')
            if cantidad == '':
                cantidad = 0
            for _ in range(int(cantidad)):
                print(f'Se esta agregando el producto {p.nombre}, {cantidad} veces, a la venta {venta.id}')
                Carrito.objects.create(id_producto=p, id_venta=venta)
        monto_pagado = sum([carrito.id_producto.precio for carrito in Carrito.objects.filter(id_venta=venta)])
        venta.monto_pagado = monto_pagado
        venta.save()
        return redirect('read_ventas')
    else:
        data = {'venta':venta, 'productos':productos}
        return render(request, 'vendedor/ventas/add_producto_venta.html', data)