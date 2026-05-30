# 👤 2. Los clientes
#Toda persona que viene a consultar, aunque no compre. Necesito tenerlos cargados para poder llamar después y ofrecer cosas. Necesito:
#-	Registrar a un cliente nuevo cuando viene a consultar por primera vez.
#-	Listar a todos los clientes.
#-	Buscar a un cliente por DNI o por nombre.
#-	Actualizar sus datos de contacto.
#-	Eliminar a quien pidió no figurar más en la base.
#De cada cliente quiero guardar:
#-	Un número interno (único).
#-	DNI.
#-	Nombre completo.
#-	Teléfono.
#-	Email (si tiene).
#-	Localidad (para saber de dónde nos llegan los clientes).
#-	Qué está buscando (un breve texto: "auto familiar barato", "una camioneta 4x4", etc.).
#-	También me gustaría poder ver, cuando consulto a un cliente, 
#   qué autos compró con nosotros y qué reservas tiene activas.


listas_Clientes = []
id_Cliente = 1

def registrar_Cliente():
    global id_Cliente, listas_Clientes
    DNI_Cliente = input("Ingrese el DNI del cliente: ")
    nombre_completo_Cliente = input("Ingrese el nombre completo del cliente: ")
    telefono_Cliente = input("Ingrese el teléfono del cliente: ")
    mail_Cliente = input("Ingrese el correo electrónico del cliente: ")
    localidad_Cliente = input("Ingrese la localidad del cliente: ")
    que_busca_Cliente = input("Ingrese que busca el cliente: ")

    nuevo_Cliente = {
        "id": id_Cliente,
        "DNI": DNI_Cliente,
        "nombre_completo": nombre_completo_Cliente,
        "telefono": telefono_Cliente,
        "mail": mail_Cliente,
        "localidad": localidad_Cliente,
        "que_busca": que_busca_Cliente
    }
    id_Cliente += 1
    listas_Clientes.append(nuevo_Cliente)


# global id_Cliente, listas_Clientes
# se uso variable global para poder usar las variables id_Cliente y listas_Clientes 
# dentro de la función registrar_Cliente() 
# y poder modificar su valor. De esta manera, cada vez que se registre un nuevo cliente, 
# se incrementará el id_Cliente y se agregará el nuevo cliente a la lista listas_Clientes.
 

def listar_Clientes():
    if len(listas_Clientes) == 0:
        print("No hay clientes registrados")
    
    for cliente in listas_Clientes:
        print(f"ID: {cliente['id']}")
        print(f"DNI: {cliente['DNI']}")
        print(f"Nombre completo: {cliente['nombre_completo']}")
        print(f"Teléfono: {cliente['telefono']}")
        print(f"Email: {cliente['mail']}")
        print(f"Localidad: {cliente['localidad']}")
        print(f"Qué busca: {cliente['que_busca']}")
        print("-" * 20)
    # print("-" * 20) se uso para imprimir una línea de guiones después de mostrar la información de cada cliente,
    # lo que ayuda a separar visualmente los datos de cada cliente en la salida.    
    #  if len(listas_Clientes) == 0:
    # print("No hay clientes registrados") esto se uso para verificar si la lista esta vacia, y asi mostrar un mensaje al usuario
    # indicando que no hay clientes registrados. Si la lista esta vacia, 
    # se imprime el mensaje y no se ejecuta el bucle for para mostrar los clientes.  
    
def buscar_Cliente():
        opcion = input("¿Buscar por?\n1. id\n2. Nombre\n3. DNI\nIngrese una opción: ")
        if opcion == "1":
            criterio_busqueda = "id"
        elif opcion == "2":
            criterio_busqueda = "nombre_completo"
        elif opcion == "3":
            criterio_busqueda = "DNI"
        else:
            print("Opción no válida.")
            return

        valor_busqueda = input(f"Ingrese el {criterio_busqueda}: ")
        if criterio_busqueda == "id":
                valor_busqueda = int(valor_busqueda)
        for cliente in listas_Clientes:
            if cliente[criterio_busqueda] == valor_busqueda:
                print(f"ID: {cliente['id']}")
                print(f"DNI: {cliente['DNI']}")
                print(f"Nombre completo: {cliente['nombre_completo']}")
                print(f"Teléfono: {cliente['telefono']}")
                print(f"Email: {cliente['mail']}")
                print(f"Localidad: {cliente['localidad']}")
                print(f"Qué busca: {cliente['que_busca']}")
                print("-" * 20)
                return
        print("Cliente no encontrado.")
        
        
def actualizar_Cliente():
    id_busqueda = int(input("Ingrese el ID del cliente a actualizar: "))
    for cliente in listas_Clientes:
        if cliente["id"] == id_busqueda:
            print("Cliente encontrado. Ingrese los nuevos datos (deje en blanco para mantener el valor actual):")
            nuevo_DNI = input(f"DNI ({cliente['DNI']}): ")
            nuevo_nombre_completo = input(f"Nombre completo ({cliente['nombre_completo']}): ")
            nuevo_telefono = input(f"Teléfono ({cliente['telefono']}): ")
            nuevo_mail = input(f"Email ({cliente['mail']}): ")
            nueva_localidad = input(f"Localidad ({cliente['localidad']}): ")
            nuevo_que_busca = input(f"Qué busca ({cliente['que_busca']}): ")

            if nuevo_DNI:
                cliente["DNI"] = nuevo_DNI
            if nuevo_nombre_completo:
                cliente["nombre_completo"] = nuevo_nombre_completo
            if nuevo_telefono:
                cliente["telefono"] = nuevo_telefono
            if nuevo_mail:
                cliente["mail"] = nuevo_mail
            if nueva_localidad:
                cliente["localidad"] = nueva_localidad
            if nuevo_que_busca:
                cliente["que_busca"] = nuevo_que_busca

            print("Cliente actualizado exitosamente.")
            return
    print("Cliente no encontrado.")
    
def eliminar_Cliente():
    id_busqueda = int(input("Ingrese el ID del cliente a eliminar: "))
    for i, cliente in enumerate(listas_Clientes):
        if cliente["id"] == id_busqueda:
            confirmacion = input(f"¿Está seguro que desea eliminar al cliente {cliente['nombre_completo']}? (s/n): ")
            if confirmacion.lower() == 's':
                del listas_Clientes[i]
                print("Cliente eliminado exitosamente.")
            else:
                print("Eliminación cancelada.")
            return
    print("Cliente no encontrado.")
    
while True:
    print("\nMenú de Clientes:")
    print("1. Registrar cliente")
    print("2. Listar clientes")
    print("3. Buscar cliente")
    print("4. Actualizar cliente")
    print("5. Eliminar cliente")
    print("6. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_Cliente()
    elif opcion == "2":
        listar_Clientes()
    elif opcion == "3":
        buscar_Cliente()
    elif opcion == "4":
        actualizar_Cliente()
    elif opcion == "5":
        eliminar_Cliente()
    elif opcion == "6":
        print("Saliendo del programa. Que tengas buen dia!!!")
        break
    else:
        print("Opción no válida. Por favor, intente nuevamente.")
    