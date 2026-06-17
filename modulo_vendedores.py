import json

RUTA_DB_VENDEDORES = "db/db_vendedores.json"

def cargar_vendedores():
    try:
        with open(RUTA_DB_VENDEDORES, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_vendedores(lista):
    with open(RUTA_DB_VENDEDORES, "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=4)

lista_vendedores = []
id_vendedor = 1


def registrar_vendedor():
    global id_vendedor

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
        "comision_porcentaje": float(comision) if comision else 0.0,
        "fecha_ingreso": fecha_ingress,
        "estado": estado,
    }

    lista_vendedores.append(vendedor)
    guardar_vendedores(lista_vendedores)
    id_vendedor += 1
    print("Vendedor registrado exitosamente.")


def listar_vendedores():
    if len(lista_vendedores) == 0:
        print("No hay vendedores registrados.")
        return

    for vendedor in lista_vendedores:
        print(f"ID: {vendedor['id']}")
        print(f"DNI: {vendedor['dni']}")
        print(f"Nombre: {vendedor['nombre_completo']}")
        print(f"Teléfono: {vendedor['telefono']}")
        print(f"Email: {vendedor['email']}")
        print(f"Comisión: {vendedor['comision_porcentaje']}%")
        print(f"Fecha ingreso: {vendedor['fecha_ingreso']}")
        print(f"Estado: {vendedor['estado']}")
        print("-" * 20)


def buscar_vendedor():
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

    for vendedor in lista_vendedores:
        if vendedor[criterio] == valor:
            print(f"ID: {vendedor['id']}")
            print(f"DNI: {vendedor['dni']}")
            print(f"Nombre: {vendedor['nombre_completo']}")
            print(f"Teléfono: {vendedor['telefono']}")
            print(f"Email: {vendedor['email']}")
            print(f"Comisión: {vendedor['comision_porcentaje']}%")
            print(f"Fecha ingreso: {vendedor['fecha_ingreso']}")
            print(f"Estado: {vendedor['estado']}")
            return

    print("Vendedor no encontrado.")


def actualizar_vendedor():
    id_busqueda = int(input("Ingrese el ID del vendedor a actualizar: "))

    for vendedor in lista_vendedores:
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
                vendedor["comision_porcentaje"] = float(nueva_comision) if nueva_comision else vendedor["comision_porcentaje"]
            if nueva_fecha:
                vendedor["fecha_ingreso"] = nueva_fecha
            if nuevo_estado:
                vendedor["estado"] = nuevo_estado

            guardar_vendedores(lista_vendedores)
            print("Vendedor actualizado correctamente.")
            return

    print("Vendedor no encontrado.")


def eliminar_vendedor():
    id_busqueda = int(input("Ingrese el ID del vendedor a eliminar: "))

    for i, vendedor in enumerate(lista_vendedores):
        if vendedor["id"] == id_busqueda:
            confirmacion = input(
                f"¿Desea eliminar al vendedor {vendedor['nombre_completo']}? (s/n): "
            )

            if confirmacion.lower() == "s":
                del lista_vendedores[i]
                guardar_vendedores(lista_vendedores)
                print("Vendedor eliminado correctamente.")
            else:
                print("Eliminación cancelada.")

            return

    print("Vendedor no encontrado.")


def menu_vendedores():
    global lista_vendedores, id_vendedor
    lista_vendedores = cargar_vendedores()
    if len(lista_vendedores) > 0:
        id_vendedor = max(v["id"] for v in lista_vendedores) + 1
    else:
        id_vendedor = 1

    while True:
        print("\n--- Menú de Vendedores ---")
        print("1. Registrar vendedor")
        print("2. Listar vendedores")
        print("3. Buscar vendedor")
        print("4. Actualizar vendedor")
        print("5. Eliminar vendedor")
        print("0. Volver al menú principal")

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
