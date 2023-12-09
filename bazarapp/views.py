from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from datetime import datetime
import re
import json
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from .models import Producto, Venta, Jornada, Carrito, Factura
from .forms import FormProducto, FormFactura
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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
    error_message = ''

    if request.method == "POST":
        form = FormProducto(request.POST)
        if form.is_valid():
            if form.cleaned_data['precio'] < 10:
                error_message = 'En este bazar contaremos con productos con un precio mayor a $10.'
            else:
                form.save()
                return read_productos(request)

    data = {'form': form, 'valor':'Agregar', 'desc':'Agregue los datos del productos que desea agregar:', 'error_message': error_message}
    return render(request, 'jefe_de_ventas/productos/add_producto.html', data)

@user_passes_test(es_jefe_de_ventas)
def edit_producto(request, id):
    p = Producto.objects.get(id = id)
    form = FormProducto(instance=p)
    error_message = ''

    if request.method == "POST":
        form = FormProducto(request.POST, instance=p)
        if form.is_valid():
            if form.cleaned_data['precio'] < 10:
                error_message = 'En este bazar contaremos con productos con un precio mayor a $10.'
            else:
                form.save()
                return read_productos(request)

    data = {'form': form, 'valor':'Editar', 'desc':'Modifique los datos del productos que decia cambiar:', 'error_message': error_message}
    return render(request, 'jefe_de_ventas/productos/add_producto.html', data)

@user_passes_test(es_jefe_de_ventas)
def del_producto(request, id):
    p = Producto.objects.get(id = id)
    p.delete()
    return read_productos(request)

@user_passes_test(es_jefe_de_ventas)
def read_jornadas(request):
    jornadas = Jornada.objects.all()
    jornada_abierta = Jornada.objects.filter(estado=True).first()
    data = {'jornadas':jornadas, 'jornada_abierta':jornada_abierta}
    return render(request, 'jefe_de_ventas/jornadas/read_jornadas.html', data)

@user_passes_test(es_jefe_de_ventas)
def abrir_jornada(request):
    jornada_abierta = Jornada.objects.filter(estado=True).first()
    if not jornada_abierta:
        Jornada.objects.create(estado=True, fecha_inicio=timezone.now())
    return redirect('read_jornadas')

@user_passes_test(es_jefe_de_ventas)
def cerrar_jornada(request):
    jornada_abierta = Jornada.objects.filter(estado=True).first()
    if jornada_abierta:
        jornada_abierta.estado = False
        jornada_abierta.fecha_cierre = timezone.now()
        jornada_abierta.save()
    return redirect('read_jornadas')
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
        ventas = Venta.objects.filter(id_jornada=Jornada.objects.filter(estado=True).first(), monto_pagado__isnull=False)
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
    
def add_producto_venta(request, id):
    venta = Venta.objects.get(id=id)
    productos = Producto.objects.all()
    if request.method == 'POST':
        if 'volver' in request.POST:  # Si el botón "Volver" fue presionado
            venta.delete()  # Eliminar la venta
            return redirect('/vendedor/read_ventas/')  # Redirigir al usuario
        factura = request.POST.get('factura')
        carritos = []
        # Verificar si todos los campos de cantidad están vacíos
        if all(not request.POST.get(f'cantidad_{p.id}') for p in productos):
            messages.error(request, 'Este campo es obligatorio')
            data = {'venta':venta, 'productos':productos}
            return render(request, 'vendedor/ventas/add_producto_venta.html', data)  # Mantener en la misma vista
        for p in productos:
            cantidad = request.POST.get(f'cantidad_{p.id}')
            if cantidad:  # Si el campo de cantidad no está vacío
                cantidad = int(cantidad)
                if cantidad < 1 or cantidad > 30:  # Si la cantidad no es un número positivo o es mayor que 30
                    messages.error(request, 'La cantidad debe ser un número positivo y no más de 30')
                    data = {'venta':venta, 'productos':productos}
                    return render(request, 'vendedor/ventas/add_producto_venta.html', data)  # Mantener en la misma vista
                for _ in range(cantidad):
                    print(f'Se esta agregando el producto {p.nombre}, {cantidad} veces, a la venta {venta.id}')
                    carrito = Carrito.objects.create(id_producto=p, id_venta=venta, cantidad_productos=cantidad)
                    carritos.append(carrito)
        if not carritos:  # Si no se ha agregado ningún producto al carrito
            venta.delete()  # Eliminar la venta
            return redirect('/vendedor/')  # Redirigir a la página anterior
        if factura is not None:  # Si el checkbox de "factura" está marcado
            return redirect(f'/vendedor/add_factura/{id}')  # Redirigir al usuario a la vista add_factura
        else:
            monto_pagado = 0  # Inicializar monto_pagado a 0
            monto_pagado += sum([carrito.id_producto.precio for carrito in carritos])
            venta.monto_pagado = monto_pagado
            venta.save()  # Guardar la venta
            return redirect('venta_detalle', id=venta.id)  # Redirigir a la vista de detalles de la venta
    else:
        data = {'venta':venta, 'productos':productos}
        return render(request, 'vendedor/ventas/add_producto_venta.html', data)
    
@transaction.atomic
def add_factura(request, id):
    venta = Venta.objects.get(id=id)
    form = FormFactura(request.POST or None)
    errors = {}

    if request.method == "POST":
        if 'cancelar' in request.POST:
            return redirect('read_ventas')

        if form.is_valid():
            factura = form.save(commit=False)  # No guardes la factura todavía

            # Realiza las validaciones
            if not re.match(r'^9\d{8}$', factura.fono):
                errors['fono'] = ['El teléfono debe contener 9 dígitos numéricos y comenzar con un 9.']
            if not re.match(r'^[a-zA-Z\s]+$', factura.comuna):
                errors['comuna'] = ['La comuna debe contener solo letras.']
            if not re.match(r'^[a-zA-Z\s]+$', factura.razon_social):
                errors['razon_social'] = ['La razón social debe contener solo letras.']
            if not re.match(r'^\d{7,8}-[\dkK]$', factura.rut):
                errors['rut'] = ['El RUT no es válido. Debe tener entre 9 y 10 dígitos (incluyendo el guión), sin puntos y con guión seguido de un número o una k. (ej. 20548956-5).']
            if len([char for char in factura.direccion if char.isalpha()]) < 5:
                errors['direccion'] = ['La dirección debe contener al menos 5 letras.']

            # Si hay errores, se mantiene en 'factura.html'
            if errors:
                data = {'form': form, 'errors': json.dumps(errors)}
                return render(request, 'vendedor/ventas/factura.html', data)

            # Si no hay errores, guarda la factura y la venta
            factura.save()
            venta.id_factura = factura  # Asigna la factura a la venta
            venta.fecha_venta = datetime.now()  # Establece la fecha de la venta

            # Lógica para guardar ventas con factura
            carritos = Carrito.objects.filter(id_venta=venta)
            monto_pagado = 0  # Inicializar monto_pagado a 0
            monto_pagado += sum([carrito.id_producto.precio for carrito in carritos])
            venta.monto_pagado = monto_pagado

            venta.save()  # Guarda la venta
            return redirect('factura_detalle', id=factura.id)

    data = {'form': form, 'errors': json.dumps(errors)}
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
    
def read_informes(request):
    return render(request, 'vendedor/informes/read_informes.html')

def pdf_creator(request):
    # Obtén la jornada abierta
    jornada_abierta = Jornada.objects.filter(estado=True).first()

    # Si no hay jornada abierta, maneja el error
    if jornada_abierta is None:
        return HttpResponse('No hay jornada abierta')

    # Obtén las ventas de la jornada abierta
    ventas_factura = Venta.objects.filter(id_jornada=jornada_abierta, id_factura__isnull=False)
    ventas_boleta = Venta.objects.filter(id_jornada=jornada_abierta, id_factura__isnull=True)

    # Crea el buffer para el PDF
    buffer = io.BytesIO()

    # Crea el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Crea una lista para los elementos del PDF
    elements = []

    # Obtiene los estilos de muestra
    styles = getSampleStyleSheet()

    # Añade un título al PDF
    title = Paragraph("Ventas de la jornada", styles['Title'])
    elements.append(title)

    # Añade un espacio
    elements.append(Spacer(1, 12))

    # Añade la información de cada venta a los elementos del PDF
    subtitle_factura = Paragraph("Ventas con factura", styles['Heading2'])
    elements.append(subtitle_factura)

    # Inicializar la suma de facturas
    suma_facturas = 0
    for venta in ventas_factura:
        if venta.monto_pagado is not None:  # Verificar si monto_pagado no es None
            venta_info = Paragraph(f"Total pagado: {venta.monto_pagado} | Vendedor: {venta.usuario}, | Fecha: {venta.fecha}", styles['Normal'])
            elements.append(venta_info)
            suma_facturas += venta.monto_pagado

    # Añadir la suma de facturas al PDF
    elements.append(Paragraph(f"Total de las Facturas: {suma_facturas}", styles['Normal']))

    subtitle_boleta = Paragraph("Ventas con boleta", styles['Heading2'])
    elements.append(subtitle_boleta)

    # Inicializar la suma de boletas
    suma_boletas = 0
    for venta in ventas_boleta:
        if venta.monto_pagado is not None:  # Verificar si monto_pagado no es None
            venta_info = Paragraph(f"Total pagado: {venta.monto_pagado} | Vendedor: {venta.usuario}, | Fecha: {venta.fecha}", styles['Normal'])
            elements.append(venta_info)
            suma_boletas += venta.monto_pagado
    # Añadir la suma de boletas al PDF
    elements.append(Paragraph(f"Total de las boletas: {suma_boletas}", styles['Normal']))
    
    # Calcular la suma total
    suma_total = suma_facturas + suma_boletas

    # Añadir la suma total al PDF
    subtitle_totales = Paragraph("Total final de las ventas de la Jornada", styles['Heading2'])
    elements.append(subtitle_totales)
    elements.append(Paragraph(f"Total de las ventas de la Jornada: {suma_total}", styles['Normal']))

    # Construye el PDF
    doc.build(elements)

    # Configura la respuesta con el PDF
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"Jornada {jornada_abierta.id}.pdf")

def venta_detalle(request, id):
    venta = Venta.objects.get(id=id)
    productos = {}
    for carrito in venta.carrito_set.all():
        productos[carrito.id_producto.nombre] = carrito.cantidad_productos
    return render(request, 'vendedor/ventas/venta_detalle.html', {'venta': venta, 'productos': productos})

def factura_detalle(request, id):
    factura = Factura.objects.get(id=id)
    venta = factura.venta_set.first()  # obtén la venta asociada
    productos = {}
    for carrito in venta.carrito_set.all():
        productos[carrito.id_producto.nombre] = carrito.cantidad_productos
    monto_pagado = venta.monto_pagado  # obtén el monto pagado de la venta
    return render(request, 'vendedor/facturas/factura_detalle.html', {'factura': factura, 'productos': productos, 'monto_pagado': monto_pagado})

def read_facturas(request):
    facturas = Factura.objects.all()  # obtén todas las facturas
    return render(request, 'vendedor/facturas/read_facturas.html', {'facturas': facturas})