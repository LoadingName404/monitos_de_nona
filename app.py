import mysql.connector
print('Conectando con la base de datos...')

noterminado = "Opcion aun no hecha"
novalido= "La opcion ingresada no es valida."
# i para los ciclos
iniciar_sesion = True #Ciclo inicio de secion
iConectarseDB = True #Ciclo para intentar conectarse a la base de datos
iPreguntarConectarseDB = True #Ciclo para preguntar si intentar otra vez conectarse a la base de datos


while iConectarseDB == True:
    try:
        conexion = mysql.connector.connect(host="sql.chukman.online",user="monitosnona",password="Inacap.2022",database="monitosnona",)
        print('Conexion exitosa')
        iConectarseDB = False
    except:
        print('No se pudo conectar con la base de datos')
        iPreguntarConectarseDB = True
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
            ############ Para conectarse a la base de datos con la ip local, se borrara al terminar el codigo ############
            elif opcion == 'local':
                try:
                    conexion = mysql.connector.connect(host="192.168.1.141",user="monitosnona",password="Inacap.2022",database="monitosnona",)
                    print('Conexion exitosa')
                    iConectarseDB = False
                    iPreguntarConectarseDB = False
                except:
                    print('tampoco funciono')
            ##############################################################################################################
            else:
                print(novalido)
    

class Acciones:
    def iniciar_secion():
        i1 = True
        usuario = input("Ingrese el nombre de usuario: ").lower()
        cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = '{}'".format(usuario))
        resultados = cursor.fetchone()
        if resultados == None:
            print("Usuario no encontrado.")
            i1 = False
        while i1 == True:
            contra = input("Ingresa la contraseña: ")
            cursor.execute("SELECT contra FROM usuario WHERE nombre_usuario = '{}'".format(usuario,contra))
            resultados = cursor.fetchone()
            if contra != resultados[0]:
                print("Contraseña incorrecta.")
                salir = False
                while salir == False:
                    salir = input("Intenarlo otra vez?(S/N): ").lower()
                    if salir == "s" or salir == "si":
                        salir = True
                    elif salir == "n" or salir == "no":
                        salir = True
                        i1 = False
                    else:
                        print(novalido)
                        salir = False
            else:
                i1 = False
                print("Contraseña correcta.")
                cursor.execute("SELECT cargo FROM usuario WHERE nombre_usuario = '{}'".format(usuario))
                resultados = cursor.fetchone()
                if resultados[0] == 1:
                    Menus.menu_jefe()
                elif resultados[0] == 2:
                    Menus.menu_vendedor(usuario)
                else:
                    print("Aun no creamos un menu para el cajero :c")

    def obtener_producto():
        cursor.execute("SELECT * FROM producto")
        resultado = cursor.fetchone()
        while resultado != None:
            print('Producto N°{}: {}, precio: {}'.format(resultado[0],resultado[1],resultado[2]))
            resultado = cursor.fetchone()

class Acciones_desarrollador:
    def show_tables():
        cursor.execute("show tables")
        resultados = cursor.fetchall()
        for resultado in resultados:
            print(resultado)

    def select_table():
        tabla = input("Que tabla desea ver?: ")
        try:
            cursor.execute("select * from {}".format(tabla))
            resultados = cursor.fetchall()
            if resultados == "[]":
                print("la tabla esta vacia")
            else:
                for resultado in resultados:
                    print(resultado)
        except mysql.connector.Error as e:
            if e.errno == 1146:
                print("La tabla {} no existe.".format(tabla))
            else:
                raise e

    def insertar_usuario():
        usuario = input("Ingrese el nombre de usuario que se va a usar para iniciar sesion: ").lower()
        cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = '{}'".format(usuario))
        resultados = cursor.fetchone()
        if resultados != None:
            print("Usuario ya existe.")
        else:
            contra = input("Ingrese la contraseña que va a tener el usuario: ")
            i = True
            while i == True:
                cargo = input("""
1.- Jefe de ventas
2.- Vendedor
3.- Cajero
Ingrese el cargo del usuario: """)
                if cargo == "1" or cargo == "2" or cargo == "3":
                    i = False
                else:
                    print(novalido)
            nombre_completo = input("Ingrese el nombre y apellido del usuario: ")
            cursor.execute("insert into usuario(nombre_usuario,nombre_completo,contra,cargo) values('{}','{}','{}',{})".format(usuario,nombre_completo,contra,cargo))
            conexion.commit()
            
    def buscar_usuario():
        usuario = input("Ingrese nombre de usuario: ")
        cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = '{}'".format(usuario))
        resultados = cursor.fetchall()
        if resultados == None:
            print("Usuario no encontrado.")
        else:
            print(resultados)

    def actualizar_usuario():
        usuario = input("Ingrese nombre de usuario que desea actualizar: ")
        cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = '{}'".format(usuario))
        resultados = cursor.fetchone()
        if resultados == None:
            print("Usuario no encontrado.")
        else:
            opcion = input('''Que desea actualizar?
1.- nombre
2.- contraseña
3.- cargo
Opcion: ''')
            if opcion == '1':
                update = input("Ingrese el cambio: ")
                cursor.execute("UPDATE usuario SET nombre_usuario = '{}' WHERE nombre_usuario = '{}'".format(update,usuario))
            elif opcion == '2':
                update = input("Ingrese el cambio: ")
                cursor.execute("UPDATE usuario SET contra = '{}' WHERE nombre_usuario = '{}'".format(update,usuario))
            elif opcion == '3':
                update = input("Ingrese el cambio: ")
                if update == '1' or update == '2' or update == '3':
                    cursor.execute("UPDATE usuario SET cargo = {} WHERE nombre_usuario = '{}'".format(update,usuario))
                else:
                    print(novalido)
            else:
                print(novalido)
        conexion.commit()

    def borrar_usuario():
        usuario = input("Ingrese el nombre del usuario que desea borrar: ")
        cursor.execute("SELECT nombre_usuario FROM usuario WHERE nombre_usuario = '{}'".format(usuario))
        resultado = cursor.fetchone()
        if resultado == None:
            print("Usuario no encontrado.")
        else:
            cursor.execute("DELETE FROM usuario WHERE nombre_usuario = '{}'".format(usuario))
            conexion.commit()
            print("Usuario borrado")

class Acciones_vendedor:
    def crear_venta(self):
        #este codigo me quedo tan bueno que funciona incluso cuando hay productos en el almacen y no lo hice pensando en eso
        cursor.execute("INSERT INTO venta(id_usuario,fecha) VALUES({},NOW())".format(self))
        
        cursor.execute("SELECT MAX(id_venta) FROM venta")
        resultado = cursor.fetchone()
        venta = resultado[0]
        print("Usando la venta N°" + str(venta))

        cursor.execute("SELECT id_producto FROM producto")
        codProductos = cursor.fetchall()
        codProductos = [codProducto[0] for codProducto in codProductos]

        i = True
        while i == True: 
            #mostrar productos
            Acciones.obtener_producto()

            #mostrar precio total
            cursor.execute("""
            SELECT SUM(producto.precio) 
            FROM carrito 
            JOIN producto ON carrito.id_producto = producto.id_producto
            WHERE carrito.id_venta = {}""".format(venta))
            precio = cursor.fetchone()
            print("Precio total de la venta: " + str(precio[0]))


            opcion = input("Ingrese el numero del producto que quiere añadir a la venta: ")
            if int(opcion) in codProductos:
                cursor.execute("INSERT INTO carrito(id_producto,id_venta) VALUES({},{})".format(opcion,venta))
            elif opcion == "0":
                i = False
                conexion.commit()
            else:
                print(novalido)

class Acciones_jefe:
    #Acciones relacionadas con productos
    def agregar_producto():
        nombre = input("Ingrese el nombre del producto: ")
        i = True
        while i == True:
            precio = int(input("Agrege el precio del producto: "))
            if precio > 2147483647:
                print("Precio ingresado demaciado grande")
            else:
                i = False
        cursor.execute("INSERT INTO producto(nombre,precio) VALUES('{}',{})".format(nombre,precio))
        conexion.commit()

    def actualizar_producto():
        print(noterminado)

    def quitar_producto():
        Acciones.obtener_producto()
        producto = input("Ingrese el numero del producto que sea quitar: ")
        cursor.execute("DELETE FROM producto WHERE id_producto = '{}'".format(producto))
        conexion.commit()

    #Acciones relacionadas con ventas
    def obtener_ventas():
        cursor.execute("SELECT id_venta FROM venta")
        codVentas = cursor.fetchall()
        i = True
        while i == True:
            cursor.execute("SELECT * FROM venta")
            print('Ventas disponibles:')
            resultado = cursor.fetchone()
            while resultado != None:
                print('Venta N°' + str(resultado[0]) + ', Fecha: ' + str(resultado[2]))
                resultado = cursor.fetchone()
            print('0.- Regresar')
            opcion = input('Elija el numero de venta que desea ver: ')
            if opcion in str(codVentas):
                print('')
                cursor.execute('select fecha FROM venta WHERE id_venta = ' + opcion)
                fecha_venta = cursor.fetchone()
                print('Fecha que hizo la venta: {}'.format(fecha_venta[0]))

                cursor.execute('''SELECT producto.nombre
                FROM carrito 
                JOIN producto ON carrito.id_producto = producto.id_producto
                WHERE carrito.id_venta = {}'''.format(opcion))
                productos = cursor.fetchone()
                print('Productos vendidos:')
                count = 1
                while productos != None:
                    print(' {}.- {}'.format(count, productos[0]))
                    productos = cursor.fetchone()
                    count += 1
                
                cursor.execute('''SELECT SUM(producto.precio) 
                FROM carrito
                JOIN producto ON carrito.id_producto = producto.id_producto
                WHERE carrito.id_venta = {}'''.format(opcion))
                benificio = cursor.fetchone()
                print('Dinero ganado: {}$'.format(benificio[0]))
                print('')
            elif opcion == '0':
                i = False
            else:
                print(novalido)
        
    def actualizar_ventas():
        cursor.execute("SELECT id_venta FROM venta")
        codVentas = cursor.fetchall()
        i = True
        while i == True:
            cursor.execute("SELECT * FROM venta")
            print('Ventas disponibles:')
            resultado = cursor.fetchone()
            while resultado != None:
                print('Venta N°' + str(resultado[0]) + ', Fecha: ' + str(resultado[2]))
                resultado = cursor.fetchone()
            print('0.- Regresar')
            nVenta = input('Elija el numero de venta que desea actualizar: ')
            if nVenta in str(codVentas):
                print('1.- Agregar producto a la venta')
                print('2.- Quitar producto de la venta')
                opcion = input('Que desea hacer?: ')
                if opcion == '1':
                    cursor.execute("SELECT id_producto FROM producto")
                    codProductos = cursor.fetchall()
                    codProductos = [codProducto[0] for codProducto in codProductos]
                    i = True
                    while i == True: 
                        #mostrar productos
                        Acciones.obtener_producto()
                        print("0.- Confirmar cambios en venta")

                        #mostrar precio total
                        cursor.execute("""
                        SELECT SUM(producto.precio) 
                        FROM carrito 
                        JOIN producto ON carrito.id_producto = producto.id_producto
                        WHERE carrito.id_venta = {}""".format(nVenta))
                        precio = cursor.fetchone()
                        print("Precio total de la venta: " + str(precio[0]))

                        opcion = input("Ingrese el numero del producto que quiere añadir a la venta: ")
                        if int(opcion) in codProductos:
                            cursor.execute("INSERT INTO carrito(id_producto,id_venta) VALUES({},{})".format(opcion,nVenta))
                        elif opcion == "0":
                            i = False
                            conexion.commit()
                        else:
                            print(novalido)
                elif opcion == '2':
                    i = True
                    while i == True:
                        cursor.execute('SELECT id_carrito FROM carrito WHERE id_venta = {}'.format(nVenta))
                        codProductos = cursor.fetchall()
                        codProductos = [codProducto[0] for codProducto in codProductos]
                        cursor.execute('''SELECT carrito.id_carrito, producto.nombre
                        FROM carrito 
                        JOIN producto ON carrito.id_producto = producto.id_producto
                        WHERE carrito.id_venta = {}'''.format(nVenta))
                        productos = cursor.fetchone()
                        print('Productos en venta {}:'.format(nVenta))
                        while productos != None:
                            print(' {}.- {}'.format(productos[0], productos[1]))
                            productos = cursor.fetchone()
                        print('0.- Confirmar cambios en venta')
                        eProducto = input('Elija el numero del producto que desea eliminar: ')
                        print(codProductos)
                        if int(eProducto) in codProductos:
                            cursor.execute('DELETE FROM carrito WHERE id_carrito = {}'.format(eProducto))
                        elif eProducto == '0':
                            print('Confirmando...')
                            i = False
                            conexion.commit()
                        else:
                            print(novalido)

                else:
                    print(novalido)
            elif nVenta == '0':
                i = False
            else:
                print(novalido)

    def eliminar_ventas():
        cursor.execute("SELECT id_venta FROM venta")
        codVentas = cursor.fetchall()
        i = True
        while i == True:
            cursor.execute("SELECT * FROM venta")
            print('Ventas disponibles:')
            resultado = cursor.fetchone()
            while resultado != None:
                print('Venta N°' + str(resultado[0]) + ', Fecha: ' + str(resultado[2]))
                resultado = cursor.fetchone()
            print('0.- Regresar')
            opcion = input('Elija el numero de venta que desea eliminar: ')
            if opcion in str(codVentas):
                cursor.execute('DELETE FROM carrito WHERE id_venta = {}'.format(opcion))
                cursor.execute('DELETE FROM venta WHERE id_venta = {}'.format(opcion))
                conexion.commit()
                print('Venta {} eliminada'.format(opcion))
            elif opcion == '0':
                i = False
            else:
                print(novalido)


class Menus:
    def menu_vendedor(self):
        i = True
        while i == True:
            opcion = input("""
#######
#
# Menu de vendedor
#
#######
#
# 1.- Crear venta
# 2.- 
# 3.-
#
# 0.- Cerrar sesion
#
###
Opcion: """)
            if opcion == "1":
                cursor.execute("SELECT id_usuario FROM usuario WHERE nombre_usuario = '{}'".format(self))
                resultados = cursor.fetchone()
                id_usuario = int(resultados[0])
                Acciones_vendedor.crear_venta(id_usuario)
            elif opcion == "0":
                i = False
            else:
                print(novalido)

    def menu_jefe():
        i = True
        while i == True:
            opcion = input("""
#######################################
#                                     #
# Menu de jefe de ventas              #
#                                     #
#######################################
#                                     #
# Que desea hacer?                    #
# -Productos:                         #
# 1.- Agregar productos al inventario #
# 2.- Ver productos en inventario     #
# 3.- Actualizar un producto          #
# 4.- Quitar productos del inventario #
# -Ventas:                            #
# 5.- Obtener las ventas              #
# 6.- Actualizar una venta            #
# 7.- Borrar una venta                #
# -Dia:                               #
# 8.- Cerrar dia de ventas            #
# 9.- Abrir dia de ventas             #
#                                     #
# 0.- Cerrar sesion                   #
#                                     #
#######################################
Opcion: """)
            #Productos
            if opcion == "1":
                Acciones_jefe.agregar_producto()
            elif opcion == "2":
                Acciones.obtener_producto()
            elif opcion == "3":
                Acciones_jefe.actualizar_producto()
            elif opcion == "4":
                Acciones_jefe.quitar_producto()
            #Ventas
            elif opcion == "5":
                Acciones_jefe.obtener_ventas()
            elif opcion == "6":
                Acciones_jefe.actualizar_ventas()
            elif opcion == "7":
                Acciones_jefe.eliminar_ventas()
            #Dia
            elif opcion == "8":
                print(noterminado)
            elif opcion == "9":
                print(noterminado)
            #Salir
            elif opcion == "0":
                i = False
            else:
                print(novalido)

    def menu_desarrollador():
        i = True
        while i == True:
            opcion = input("""
1.- Mostrar tablas existentes
2.- Ver contenido de una tabla
3.- Insertar usuario
4.- Buscar usuario
5.- Actualizar usuario
6.- Borrar usuario

0.- Volver
: """)
            if opcion == "1":
                Acciones_desarrollador.show_tables()
            elif opcion == "2":
                Acciones_desarrollador.select_table()
            elif opcion == "3":
                Acciones_desarrollador.insertar_usuario()
            elif opcion == "4":
                Acciones_desarrollador.buscar_usuario()
            elif opcion == "5":
                Acciones_desarrollador.actualizar_usuario()
            elif opcion == "6":
                Acciones_desarrollador.borrar_usuario()
            elif opcion == "0":
                i = False
            else:
                print(novalido)
            
while iniciar_sesion == True:
    cursor = conexion.cursor()
    opcion = input("""
###################################
#                                 #
# Bienvenido al sistema de ventas #
#                                 #
###################################
#                                 #
# 1.- Iniciar secion              #
#                                 #
# 0.- Cerrar Programa             #
#                                 #
###################################
Opcion: """)

    if opcion == "1":
        Acciones.iniciar_secion()
    ############ Elif para accedor al menu de desarrollador, se borrara al terminar el codigo ############
    elif opcion == "comando":
        Menus.menu_desarrollador()
    ######################################################################################################
    elif opcion == "0":
        print("Adios.")
        iniciar_sesion = False
        conexion.close()
    else:
        print(novalido)