from utils.dbUtils import (
    _db_actualizar_un_registro,
    _db_eliminar_valor,
    _db_inyectar_datos,
    _db_leer_datos,
)
from utils.idUtils import _id_autoincremental
from utils.validateUtils import Color, _limpiar_pantalla

lista_vendedores = []


def registrar_vendedor():
    id_vendedor = _id_autoincremental("db/db_vendedores.json")

    dni = input("Ingrese DNI: ")
    nombre = input("Ingrese nombre completo: ")
    telefono = input("Ingrese teléfono: ")
    email = input("Ingrese email: ")
    comision = input("Ingrese porcentaje de comisión: ")
    fecha_ingress = input("Ingrese fecha de ingreso: ")
    estado = input("Ingrese estado (activo/inactivo): ")

    vendedor = {
        "id": id_vendedor,
        "dni": dni,
        "nombre_completo": nombre,
        "telefono": telefono,
        "email": email,
        "comision_porcentaje": comision,
        "fecha_ingreso": fecha_ingress,
        "estado": estado,
    }

    _db_inyectar_datos("db/db_vendedores.json", vendedor)
    print("Vendedor registrado exitosamente.")
    input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")


def listar_vendedores():
    vendedores = _db_leer_datos("db/db_vendedores.json")

    if len(vendedores) == 0:
        print("No hay vendedores registrados.")
        return

    for vendedor in vendedores:
        print(f"ID: {vendedor['id']}")
        print(f"DNI: {vendedor['dni']}")
        print(f"Nombre: {vendedor['nombre_completo']}")
        print(f"Teléfono: {vendedor['telefono']}")
        print(f"Email: {vendedor['email']}")
        print(f"Comisión: {vendedor['comision_porcentaje']}%")
        print(f"Fecha ingreso: {vendedor['fecha_ingreso']}")
        print(f"Estado: {vendedor['estado']}")
        print("-" * 20)

    input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")


def buscar_vendedor():
    vendedores = _db_leer_datos("db/db_vendedores.json")

    opcion = input("¿Buscar por?\n1. ID\n2. Nombre\n3. DNI\nIngrese una opción: ")

    if opcion == "1":
        criterio = "id"
    elif opcion == "2":
        criterio = "nombre_completo"
    elif opcion == "3":
        criterio = "dni"
    else:
        print("Opción no válida.")
        return

    valor = input(f"Ingrese el {criterio}: ")

    if criterio == "id":
        valor = int(valor)

    for vendedor in vendedores:
        if vendedor[criterio] == valor:
            print(f"\nID: {vendedor['id']}")
            print(f"DNI: {vendedor['dni']}")
            print(f"Nombre: {vendedor['nombre_completo']}")
            print(f"Teléfono: {vendedor['telefono']}")
            print(f"Email: {vendedor['email']}")
            print(f"Comisión: {vendedor['comision_porcentaje']}%")
            print(f"Fecha ingreso: {vendedor['fecha_ingreso']}")
            print(f"Estado: {vendedor['estado']}")
            input(f"\nPresione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")
            return
    print("Vendedor no encontrado.")


def actualizar_vendedor():
    vendedores = _db_leer_datos("db/db_vendedores.json")

    id_busqueda = int(input("Ingrese el ID del vendedor a actualizar: "))

    for vendedor in vendedores:
        if vendedor["id"] == id_busqueda:
            nuevo_dni = input(f"DNI ({vendedor['dni']}): ")
            nuevo_nombre = input(f"Nombre ({vendedor['nombre_completo']}): ")
            nuevo_telefono = input(f"Teléfono ({vendedor['telefono']}): ")
            nuevo_email = input(f"Email ({vendedor['email']}): ")
            nueva_comision = input(f"Comisión ({vendedor['comision_porcentaje']}): ")
            nueva_fecha = input(f"Fecha ingreso ({vendedor['fecha_ingreso']}): ")
            nuevo_estado = input(f"Estado ({vendedor['estado']}): ")

            if nuevo_dni:
                vendedor["dni"] = nuevo_dni
            if nuevo_nombre:
                vendedor["nombre_completo"] = nuevo_nombre
            if nuevo_telefono:
                vendedor["telefono"] = nuevo_telefono
            if nuevo_email:
                vendedor["email"] = nuevo_email
            if nueva_comision:
                vendedor["comision_porcentaje"] = nueva_comision
            if nueva_fecha:
                vendedor["fecha_ingreso"] = nueva_fecha
            if nuevo_estado:
                vendedor["estado"] = nuevo_estado

            _db_actualizar_un_registro(
                "db/db_vendedores.json", vendedor["id"], vendedor
            )
            print("Vendedor actualizado correctamente.")

            input(f"\nPresione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")
            return

    print("Vendedor no encontrado.")


def eliminar_vendedor():
    vendedores = _db_leer_datos("db/db_vendedores.json")

    id_busqueda = int(input("Ingrese el ID del vendedor a eliminar: "))

    for i, vendedor in enumerate(vendedores):
        if vendedor["id"] == id_busqueda:
            confirmacion = input(
                f"¿Desea eliminar al vendedor {vendedor['nombre_completo']}? (s/n): "
            )

            if confirmacion.lower() == "s":
                del vendedores[i]
                _db_eliminar_valor("db/db_vendedores.json", id_busqueda)
                print("Vendedor eliminado correctamente.")

                input(
                    f"\nPresione {Color.AMARILLO}ENTER{Color.RESET} para continuar..."
                )
                return
            else:
                print("Eliminación cancelada.")

            input(f"\nPresione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")
            return

    print("Vendedor no encontrado.")

    input(f"\nPresione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")


def menu_vendedores():
    while True:
        _limpiar_pantalla()
        print(f"""
     ═══════════════════════════════════════════════════
     👔 VENDEDORES
     ═══════════════════════════════════════════════════
     {Color.CYAN}1. {Color.RESET}Registrar vendedor
     {Color.CYAN}2. {Color.RESET}Listar vendedores
     {Color.CYAN}3. {Color.RESET}Buscar vendedor
     {Color.CYAN}4. {Color.RESET}Actualizar vendedor
     {Color.CYAN}5. {Color.RESET}Eliminar vendedor
     {Color.ROJO}0. {Color.RESET}Volver al menú principal
     """)
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_vendedor()
        elif opcion == "2":
            listar_vendedores()
        elif opcion == "3":
            buscar_vendedor()
        elif opcion == "4":
            actualizar_vendedor()
        elif opcion == "5":
            eliminar_vendedor()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu_vendedores()
