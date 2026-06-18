# 👤 2. Los clientes
# Toda persona que viene a consultar, aunque no compre. Necesito tenerlos cargados para poder llamar después y ofrecer cosas. Necesito:
# -	Registrar a un cliente nuevo cuando viene a consultar por primera vez.
# -	Listar a todos los clientes.
# -	Buscar a un cliente por DNI o por nombre.
# -	Actualizar sus datos de contacto.
# -	Eliminar a quien pidió no figurar más en la base.
# De cada cliente quiero guardar:
# -	Un número interno (único).
# -	DNI.
# -	Nombre completo.
# -	Teléfono.
# -	Email (si tiene).
# -	Localidad (para saber de dónde nos llegan los clientes).
# -	Qué está buscando (un breve texto: "auto familiar barato", "una camioneta 4x4", etc.).
# -	También me gustaría poder ver, cuando consulto a un cliente,
#   qué autos compró con nosotros y qué reservas tiene activas.


# 👤 Módulo de Clientes - Concesionaria
import json

from utils.validateUtils import Color, _limpiar_pantalla

RUTA_DB_CLIENTES = "db/db_clientes.json"


def cargar_clientes():
    try:
        with open(RUTA_DB_CLIENTES, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_clientes(lista):
    with open(RUTA_DB_CLIENTES, "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=4)


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
        "dni": DNI_Cliente,
        "nombre_completo": nombre_completo_Cliente,
        "telefono": telefono_Cliente,
        "email": mail_Cliente,
        "localidad": localidad_Cliente,
        "que_busca": que_busca_Cliente,
    }
    id_Cliente += 1
    listas_Clientes.append(nuevo_Cliente)
    guardar_clientes(listas_Clientes)
    print(f"{Color.VERDE}Cliente registrado exitosamente.{Color.RESET}")
    input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")


def listar_Clientes():
    if len(listas_Clientes) == 0:
        print(f"{Color.ROJO}No hay clientes registrados{Color.RESET}")
        return

    for cliente in listas_Clientes:
        print(f"{Color.CYAN}ID: {Color.RESET}{cliente['id']}")
        print(f"{Color.CYAN}DNI: {Color.RESET}{cliente['dni']}")
        print(f"{Color.CYAN}Nombre completo: {Color.RESET}{cliente['nombre_completo']}")
        print(f"{Color.CYAN}Teléfono: {Color.RESET}{cliente['telefono']}")
        print(f"{Color.CYAN}Email: {Color.RESET}{cliente['email']}")
        print(f"{Color.CYAN}Localidad: {Color.RESET}{cliente['localidad']}")
        print(f"{Color.CYAN}Qué busca: {Color.RESET}{cliente['que_busca']}")
        print("-" * 20)
    input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")


def buscar_Cliente():
    opcion = input("¿Buscar por?\n1. ID\n2. Nombre\n3. DNI\nIngrese una opción: ")
    if opcion == "1":
        criterio_busqueda = "id"
    elif opcion == "2":
        criterio_busqueda = "nombre_completo"
    elif opcion == "3":
        criterio_busqueda = "dni"
    else:
        print(f"{Color.ROJO}Opción no válida.{Color.RESET}")
        return

    valor_busqueda = input(f"Ingrese el {criterio_busqueda}: ")
    if criterio_busqueda == "id":
        valor_busqueda = int(valor_busqueda)

    for cliente in listas_Clientes:
        if cliente[criterio_busqueda] == valor_busqueda:
            print(f"\n{Color.CYAN}ID: {Color.RESET}{cliente['id']}")
            print(f"{Color.CYAN}DNI: {Color.RESET}{cliente['dni']}")
            print(
                f"{Color.CYAN}Nombre completo: {Color.RESET}{cliente['nombre_completo']}"
            )
            print(f"{Color.CYAN}Teléfono: {Color.RESET}{cliente['telefono']}")
            print(f"{Color.CYAN}Email: {Color.RESET}{cliente['email']}")
            print(f"{Color.CYAN}Localidad: {Color.RESET}{cliente['localidad']}")
            print(f"{Color.CYAN}Qué busca: {Color.RESET}{cliente['que_busca']}")
            print("-" * 20)
            input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")
            return
    print(f"{Color.ROJO}Cliente no encontrado.{Color.RESET}")


def actualizar_Cliente():
    id_busqueda = int(input("Ingrese el ID del cliente a actualizar: "))
    for cliente in listas_Clientes:
        if cliente["id"] == id_busqueda:
            print(
                "Cliente encontrado. Ingrese los nuevos datos (deje en blanco para mantener el valor actual):"
            )
            nuevo_DNI = input(f"DNI ({cliente['dni']}): ")
            nuevo_nombre_completo = input(
                f"Nombre completo ({cliente['nombre_completo']}): "
            )
            nuevo_telefono = input(f"Teléfono ({cliente['telefono']}): ")
            nuevo_mail = input(f"Email ({cliente['email']}): ")
            nueva_localidad = input(f"Localidad ({cliente['localidad']}): ")
            nuevo_que_busca = input(f"Qué busca ({cliente['que_busca']}): ")

            if nuevo_DNI:
                cliente["dni"] = nuevo_DNI
            if nuevo_nombre_completo:
                cliente["nombre_completo"] = nuevo_nombre_completo
            if nuevo_telefono:
                cliente["telefono"] = nuevo_telefono
            if nuevo_mail:
                cliente["email"] = nuevo_mail
            if nueva_localidad:
                cliente["localidad"] = nueva_localidad
            if nuevo_que_busca:
                cliente["que_busca"] = nuevo_que_busca

            guardar_clientes(listas_Clientes)
            print("Cliente actualizado exitosamente.")
            input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")
            return
    print(f"{Color.ROJO}Cliente no encontrado.{Color.RESET}")
    input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")


def eliminar_Cliente():
    id_busqueda = int(input("Ingrese el ID del cliente a eliminar: "))
    for i, cliente in enumerate(listas_Clientes):
        if cliente["id"] == id_busqueda:
            confirmacion = input(
                f"¿Está seguro que desea eliminar al cliente {cliente['nombre_completo']}? (s/n): "
            )
            if confirmacion.lower() == "s":
                del listas_Clientes[i]
                guardar_clientes(listas_Clientes)
                print(f"{Color.VERDE}Cliente eliminado exitosamente.{Color.RESET}")
                input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")
            else:
                print(f"{Color.ROJO}Eliminación cancelada.{Color.RESET}")
                input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")
            return
    print(f"{Color.ROJO}Cliente no encontrado.{Color.RESET}")


# ✅ El menú ahora está dentro de una función, no se ejecuta solo al importar
def menu_clientes():
    global listas_Clientes, id_Cliente
    listas_Clientes = cargar_clientes()
    if len(listas_Clientes) > 0:
        id_Cliente = max(cliente["id"] for cliente in listas_Clientes) + 1
    else:
        id_Cliente = 1

    while True:
        _limpiar_pantalla()
        print(f"""
    ═══════════════════════════════════════════════════
    👤 CLIENTES
    ═══════════════════════════════════════════════════
    {Color.CYAN}1. {Color.RESET}Registrar cliente
    {Color.CYAN}2. {Color.RESET}Listar clientes
    {Color.CYAN}3. {Color.RESET}Buscar cliente
    {Color.CYAN}4. {Color.RESET}Actualizar cliente
    {Color.CYAN}5. {Color.RESET}Eliminar cliente
    {Color.CYAN}0. {Color.RESET}Volver al menú principal
    """)

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
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.")


# Permite probar el módulo de forma independiente
if __name__ == "__main__":
    menu_clientes()
