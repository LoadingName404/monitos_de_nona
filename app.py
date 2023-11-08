import mysql.connector
print('Conectando con la base de datos...')

noterminado = "Opcion aun no hecha"
novalido= "La opcion ingresada no es valida."
# i para los ciclos
iniciar_sesion = True #Ciclo inicio de secion
iConectarseDB = True #Ciclo para intentar conectarse a la base de datos
iPreguntarConectarseDB = True #Ciclo para preguntar si intentar otra vez conectarse a la base de datos en caso de fallo


while iConectarseDB == True:
    try:
        conexion = mysql.connector.connect(host="chukman.online",user="monitosnona",password="Inacap.2022",database="monitosnona",)
        print('Conexion exitosa')
        iConectarseDB = False
    except:
        print('No se pudo conectar con la base de datos')
        print(mysql.connector.Error)
        while iPreguntarConectarseDB == True:
            opcion = input('Intentar denuevo?(S/N): ').lower()
            if opcion == 's' or opcion == 'si':
                print('Intentado otra vez...')
                iPreguntarConectarseDB = False
            elif opcion == 'n' or opcion == 'no':
                print('Adios')
                iConectarseDB = False
                iPreguntarConectarseDB = False
                iniciar_sesion = False
            else:
                print(novalido)
    

class Acciones:
    def iniciar_secion():
        usuario = input("Ingrese el nombre de usuario: ").lower()
        contra = input("Ingresa la contraseña: ")
        cursor.execute("SELECT contra FROM usuarios WHERE nombre_usuario = '{}'".format(usuario,contra))
        contraR = cursor.fetchone()
        if contraR == None or contra not in contraR :
            print("El usuario y contraseña no coinciden.")
        else:
            print("Contraseña correcta.")
            cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre_usuario = '{}'".format(usuario))
            id_usuarioR = cursor.fetchone()
            cursor.execute("SELECT id_cargo FROM usuarios WHERE nombre_usuario = '{}'".format(usuario))
            id_cargoR = cursor.fetchone()
            if id_cargoR[0] == 1:
                Menus.menu_vendedor(id_usuarioR)
            elif id_cargoR[0] == 2:
                Menus.menu_jefe()
            else:
                print("Aun no creamos un menu para el cajero :c")

    def obtener_producto():
        cursor.execute("SELECT * FROM productos")
        productosR = cursor.fetchone()
        while productosR != None:
            print('Producto N°{}: {}, precio: {}, SKU:{}'.format(productosR[0],productosR[1],productosR[2],productosR[3]))
            productosR = cursor.fetchone()

class Acciones_vendedor:
    def crear_venta(self):
        cursor.execute("SELECT id_jornada FROM jornadas WHERE estado = TRUE")
        jornada = cursor.fetchone()
        if jornada != None:
            cursor.execute("INSERT INTO ventas(id_usuario,fecha,id_jornada) VALUES({},NOW(),{})".format(self[0],jornada[0]))

            cursor.execute("SELECT MAX(id_venta) FROM ventas")
            id_ventaR = cursor.fetchone()
            print("Usando la venta N°" + str(id_ventaR[0]))

            ################################### Cliclo agregando los productos ###################################
            #                                                                                                    #
            precio = 0
            while True == True: 
                Acciones.obtener_producto()
                print("0.- Cerrar venta")
                print("Precio de los productos: " + str(precio) + " | Precio total con IVA: " + str(precio * 1.19))

                opcion = int(input("Ingrese el numero del producto que quiere añadir a la venta: "))
                if opcion != 0:
                    cursor.execute("INSERT INTO carritos(id_producto,id_venta) VALUES({},{})".format(opcion,id_ventaR[0]))
                    cursor.execute("SELECT precio FROM productos WHERE id_producto =" + str(opcion))
                    precio_producto = cursor.fetchone()
                    precio = precio_producto[0] + precio
                elif opcion == 0:
                    conexion.commit()
                    break
            #                                                                                                    #
            ######################################################################################################
            while True == True:
                print("1.- Boleta")
                print("2.- Factura")
                opcion = int(input("Ingrese el numero del tipo de documento que quiere el cliente: "))
                if opcion == 1:
                    break
                elif opcion == 2:
                    razon = input("Ingrese la razon social del cliente (nombre): ")
                    rut = input("Ingrese el rut del cliente: ")
                    cursor.execute("INSERT INTO facturas(razon,rut) VALUES('{}','{}')".format(razon,rut))
                    cursor.execute("SELECT MAX(id_factura) FROM facturas")
                    id_facturaR = cursor.fetchone()
                    cursor.execute("UPDATE ventas SET id_factura = {} WHERE id_venta = {}".format(id_facturaR,id_ventaR[0]))
                else:
                    print(novalido)
        else:
            print("No es posible crear ventas, no hay una jornada abierta.")

class Acciones_jefe:
    ########## Acciones relacionadas con productos ###########
    #                                                        #
    def agregar_producto():
        nombre = input("Ingrese el nombre del producto: ")
        precio = int(input("Agrege el precio del producto (sin considerar IVA): "))
        sku = input('Ingrese el SKU del producto: ')
        cursor.execute("INSERT INTO productos(nombre,precio,sku) VALUES('{}',{},'{}')".format(nombre,precio,sku))
        conexion.commit()
        print('Se ha agregado el producto al inventario.')
    #                                                        #
    def actualizar_producto():
        print(noterminado)
    #                                                        #
    def quitar_producto():
        Acciones.obtener_producto()
        producto = input("Ingrese el numero del producto que sea quitar: ")
        cursor.execute("DELETE FROM productos WHERE id_producto = '{}'".format(producto))
        conexion.commit()
        print('Se ha eliminado el producto del inventario.')
    #                                                        #
    ############ Acciones relacionadas con ventas ############
    #                                                        #
    def obtener_ventas():
        cursor.execute("SELECT id_venta FROM ventas")
        codVentas = cursor.fetchall()
        while True == True:
            cursor.execute("SELECT * FROM ventas")
            print('Ventas disponibles:')
            ventasR = cursor.fetchone()
            while ventasR != None:
                print('Venta N°' + str(ventasR[0]) + ', Fecha: ' + str(ventasR[2]))
                ventasR = cursor.fetchone()
            print('0.- Regresar')
            id_venta = int(input('Elija el numero de venta que desea ver: '))
            for tupla in codVentas:
                if id_venta in tupla:
                    print('')
                    cursor.execute('SELECT fecha FROM ventas WHERE id_venta = ' + str(id_venta))
                    fecha_venta = cursor.fetchone()
                    print('Fecha que hizo la venta: {}'.format(fecha_venta[0]))

                    cursor.execute('''SELECT productos.nombre
                    FROM carritos
                    JOIN productos ON carritos.id_producto = productos.id_producto
                    WHERE carritos.id_venta = {}'''.format(id_venta))
                    productos = cursor.fetchone()
                    print('Productos vendidos:')
                    count = 1
                    while productos != None:
                        print(' {}.- {}'.format(count, productos[0]))
                        productos = cursor.fetchone()
                        count += 1
                
                    cursor.execute('''SELECT SUM(productos.precio) 
                    FROM carritos
                    JOIN productos ON carritos.id_producto = productos.id_producto
                    WHERE carritos.id_venta = {}'''.format(id_venta))
                    benificio = cursor.fetchone()
                    print('Dinero pagado: ' + str(benificio[0]) + '$')
                    print('Dinero pagado mas impuestos: ' + str(float(benificio[0]) * 1.19) + '$')
                    print('')
                elif id_venta == 0:
                    break
                else:
                    print(novalido)
    #                                                        #
    ################ Acciones con la jornada #################
    #                                                        #
    def abrir_jornada():
        cursor.execute("SELECT estado FROM jornadas WHERE estado = TRUE")
        estadoR = cursor.fetchone()
        if estadoR != None:
            print("Ya hay una jornada abierta.")
        else:
            cursor.execute("INSERT INTO jornadas(estado,fecha_inicio,fecha_cierre) VALUES(TRUE,NOW(),NULL)")
            conexion.commit()
            cursor.execute("SELECT * FROM jornadas WHERE estado = TRUE")
            jornada = cursor.fetchone()
            print("Se ha creado una nueva jornada de ventas con el ID de {}, abierto el {}".format(jornada[0],jornada[2]))
    #                                                        #
    def cerrar_jornada():
        cursor.execute("SELECT estado FROM jornadas WHERE estado = TRUE")
        estadoR = cursor.fetchone()
        if estadoR == None:
            print("No hay ningun jornada abierto.")
        else:
            cursor.execute("UPDATE jornadas SET estado = False, fecha_cierre = NOW() WHERE estado = True")
            conexion.commit()
            cursor.execute("SELECT MAX(id_jornada) FROM jornadas")
            #jornada = cursor.fetchone()
            #print("Se ha cerrado la jornada de ventas con el ID de {}, abierto el {}".format(jornada[0],jornada[2]))
        #ahora
    #                                                        #
    ############### Acciones con los usurios #################
    #                                                        #
    def insertar_usuario():
        usuario = input("Ingrese el nombre de usuario que se va a usar para iniciar sesion: ")
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = '" + usuario + "'")
        usuarioR = cursor.fetchone()
        if usuarioR != None:
            print("Usuario ya existe.")
        else:
            contra = input("Ingrese la contraseña que va a tener el usuario: ")
            while True == True:
                cargo = input("""
1.- Vendedor
2.- Jefe de ventas
Ingrese el cargo del usuario: """)
                if cargo == "1" or cargo == "2":
                    break
                else:
                    print(novalido)
            nombre_completo = input("Ingrese el nombre y apellido del usuario: ")
            cursor.execute("insert into usuarios(nombre_usuario,nombre_completo,contra,id_cargo) values('{}','{}','{}',{})".format(usuario,nombre_completo,contra,cargo))
            conexion.commit()
    #                                                        #
    def obtener_usuarios():
        cursor.execute("SELECT * FROM usuarios JOIN cargos ON usuarios.id_cargo = cargos.id_cargo")
        usuariosR = cursor.fetchone()
        print("ID | nombre de usuario | nombre completo | contraseña | cargo")
        while usuariosR != None:
            print("{} | {} | {} | {} | {}".format(usuariosR[0],usuariosR[1],usuariosR[2],usuariosR[3],usuariosR[6]))
            usuariosR = cursor.fetchone()
    #                                                        #
    def actualizar_usuario():
        Acciones_jefe.obtener_usuarios()
        id_usuario = input("Ingrese el id del usuario que desea actualizar: ")
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = {}".format(id_usuario))
        id_usuarioR = cursor.fetchone()
        if id_usuarioR == None:
            print("Usuario no encontrado.")
        else:
            opcion = input('''Que desea actualizar?
1.- nombre
2.- contraseña
3.- cargo
Opcion: ''')
            if opcion == '1':
                atrivuto = 'nombre'
            elif opcion == '2':
                atrivuto = 'contra'
            elif opcion == '3':
                atrivuto = 'id_cargo'
            else:
                print(novalido)
            update = input("Ingrese el cambio: ")
            cursor.execute("UPDATE usuarios SET {} = {} WHERE id_usuario = {}".format(atrivuto,update,id_usuario))
    #                                                        #
    def borrar_usuario():
        Acciones_jefe.obtener_usuarios
        id_usuario = input("Ingrese el ID del usuario que desea borrar: ")
        cursor.execute("SELECT nombre_usuario FROM usuarios WHERE id_usuario = {}".format(id_usuario))
        resultado = cursor.fetchone()
        if resultado == None:
            print("Usuario no encontrado.")
        else:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = {}".format(id_usuario))
            conexion.commit()
            print("Usuario borrado")
    #                                                        #
    ##########################################################
class Menus:
    def menu_vendedor(self):
        while True == True:
            opcion = int(input("""
+++++++++++++++++++++
+                   +
+ Menu de vendedor  +
+                   +
+++++++++++++++++++++
+                   +
+ 1.- Crear venta   +
+                   +
+ 0.- Cerrar sesion +
+                   +
+++++++++++++++++++++
Opcion: """))
            if opcion == 1:
                Acciones_vendedor.crear_venta(self)
            elif opcion == 0:
                break
            else:
                print(novalido)

    def menu_jefe():
        while True == True:
            opcion = int(input("""
++++++++++++++++++++++++++++++++++++++
+                                    +
+ Menu de jefe de ventas             +
+                                    +
++++++++++++++++++++++++++++++++++++++
+                                    +
+ Que desea hacer?                   +
+                                    +
+ 1.- Administrar productos          +
+ 2.- Obtener ventas resgistradas    +
+ 3.- Administrar usuarios           +
+ 4.- Administrar jornadas           +
+ 5.- Administrar informes de ventas +
+                                    +
+ 0.- Cerrar secion                  +
+                                    +
++++++++++++++++++++++++++++++++++++++
Opcion: """))
            if opcion == 1:
                Menus_jefe.productos()
            elif opcion == 2:
                Acciones_jefe.obtener_ventas()
            elif opcion == 3:
                Menus_jefe.usuarios()
            elif opcion == 4:
                Menus_jefe.jornada()
            elif opcion == 5:
                Menus_jefe.informes()
            elif opcion == 0:
                break
            else:
                print(novalido)

    def menu_desarrollador():
        while True == True:
            opcion = input("""
1.- Insertar usuario
2.- Obtener usuarios
3.- Actualizar usuario
4.- Borrar usuario

0.- Volver
: """)
            if opcion == "1":
                Acciones_jefe.insertar_usuario()
            elif opcion == "2":
                Acciones_jefe.obtener_usuarios()
            elif opcion == "3":
                Acciones_jefe.actualizar_usuario()
            elif opcion == "4":
                Acciones_jefe.borrar_usuario()
            elif opcion == "0":
                break
            else:
                print(novalido)

class Menus_jefe:
    def productos():
        while True == True:
            opcion = int(input("""
+++++++++++++++++++++++++++++++++++++++++
+                                       +
+ Menu de administracion de productos   +
+                                       +
+++++++++++++++++++++++++++++++++++++++++
+                                       +
+ Que desea hacer?                      +
+                                       +
+ 1.- Agregar productos al inventario   +
+ 2.- Ver productos en inventario       +
+ 3.- Actualizar producto en inventario +
+ 4.- Eliminar prodcuto en inventario   +
+                                       +
+ 0.- Volver                            +
+                                       +
+++++++++++++++++++++++++++++++++++++++++
Opcion: """))
            if opcion == 1:
                Acciones_jefe.agregar_producto()
            elif opcion == 2:
                Acciones.obtener_producto()
            elif opcion == 3:
                Acciones_jefe.actualizar_producto()
            elif opcion == 4:
                Acciones_jefe.quitar_producto()
            elif opcion == 0:
                break
            else:
                print(novalido)

    def usuarios():
        while True == True:
            opcion = int(input("""
++++++++++++++++++++++++++++++++++++++
+                                    +
+ Menu de administracion de usuarios +
+                                    +
++++++++++++++++++++++++++++++++++++++
+                                    +
+ Que desea hacer?                   +
+                                    +
+ 1.- Añadir usuario                 +
+ 2.- Ver usuarios                   +
+ 3.- Actualizar usuario             +
+ 4.- Eliminar usuario               +
+                                    +
+ 0.- Volver                         +
+                                    +
++++++++++++++++++++++++++++++++++++++
Opcion: """))
            if opcion == 1:
                Acciones_jefe.insertar_usuario()
            elif opcion == 2:
                Acciones_jefe.obtener_usuarios()
            elif opcion == 3:
                Acciones_jefe.actualizar_usuario()
            elif opcion == 4:
                Acciones_jefe.borrar_usuario()
            elif opcion == 0:
                break
            else:
                print(novalido)

    def jornada():
        while True == True:
            opcion = int(input("""
++++++++++++++++++++++++++++++++++++++++
+                                      +
+ Menu de administracion de la jornada +
+                                      +
++++++++++++++++++++++++++++++++++++++++
+                                      +
+ Que desea hacer?                     +
+                                      +
+ 1.- Abrir jornada de ventas          +
+ 2.- Cerrar jornada de ventas         +
+                                      +
+ 0.- Volver                           +
+                                      +
++++++++++++++++++++++++++++++++++++++++
Opcion: """))
            if opcion == 1:
                Acciones_jefe.abrir_jornada()
            elif opcion == 2:
                Acciones_jefe.cerrar_jornada()
            elif opcion == 0:
                break
            else:
                print(novalido)
    
    def informes():
        print(noterminado)

while iniciar_sesion == True:
    cursor = conexion.cursor()
    opcion = int(input("""
+++++++++++++++++++++++++++++++++++
+                                 +
+ Bienvenido al sistema de ventas +
+                                 +
+++++++++++++++++++++++++++++++++++
+                                 +
+ 1.- Iniciar secion              +
+                                 +
+ 0.- Cerrar Programa             +
+                                 +
+++++++++++++++++++++++++++++++++++
Opcion: """))

    if opcion == 1:
        Acciones.iniciar_secion()
    elif opcion == 2:
        Menus.menu_desarrollador()
    elif opcion == 0:
        print("Adios.")
        iniciar_sesion = False
        conexion.close()
    else:
        print(novalido)
