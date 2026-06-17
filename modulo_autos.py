# date, fecha de ingreso al stock, al importar date se crea con fecha real
import json
from datetime import date

# print("=== EL PROGRAMA ESTA ARRANCANDO CORRECTAMENTE ===")

RUTA_DB_AUTOS = "db/db_autos.json"

def cargar_autos():
    try:
        with open(RUTA_DB_AUTOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_autos(lista):
    with open(RUTA_DB_AUTOS, "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, indent=4)

lista_autos = []
siguiente_id_auto = 1


def pedir_entero(mensaje):
    while True:  # dentro de un bucle, convierte la entrada a numero
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:  ###use escept si el usuario se equivoca en datos de km o precio el prog se cierra y no carga
            print("Error: Ingrese un numero entero valido.")


def pedir_estado_valido():
    estados_permitidos = [
        "disponible",
        "reservado",
        "vendido",
        "en taller",
    ]  # 4 pautas pedidas por el dueño
    while True:
        estado = (
            input("Ingrese estado (disponible/reservado/vendido/en taller): ")
            .lower()
            .strip()
        )  # minuscula y borra los espacios en blanco
        if (
            estado in estados_permitidos
        ):  # busca dentro de la lista el estado valido, si no esta vuelve a preg. con while
            return estado
        print("Estado invalido.")


def cargar_auto_nuevo():
    global siguiente_id_auto
    print("\n--- CARGAR NUEVO AUTO ---")
    patente = (
        input("Patente: ").upper().strip()
    )  # mayusculas y sin espacios para la patente y avitar errores de carga y busqueda
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    anio = pedir_entero("Año: ")
    kilometros = pedir_entero("Kilometros: ")
    precio = pedir_entero("Precio de venta: ")
    estado = pedir_estado_valido()
    fecha_actual = date.today()

    ##diccionario para registro del auto
    nuevo_auto = {
        "id": siguiente_id_auto,
        "patente": patente,
        "marca": marca,
        "modelo": modelo,
        "anio": anio,
        "kilometros": kilometros,
        "precio": precio,
        "estado": estado,
        "fecha_ingreso": str(fecha_actual),
    }
    lista_autos.append(nuevo_auto)
    guardar_autos(lista_autos)
    print("Auto cargado con exito.")
    siguiente_id_auto += 1  # suma 1 a la variable global


def ver_listado_autos():
    print("\n--- LISTADO DE AUTOS EN STOCK ---")
    if not lista_autos:
        print("No hay autos.")
        return
    print("Filtros? (0: Sin filtro, 1: Por Marca, 2: Por Estado)")
    opcion_filtro = input("Seleccione opcion: ")
    marca_buscar = ""
    estado_buscar = ""
    if opcion_filtro == "1":
        marca_buscar = input("Marca a filtrar: ").lower().strip()
    elif opcion_filtro == "2":
        estado_buscar = input("Estado a filtrar: ").lower().strip()

    for auto in lista_autos:
        if opcion_filtro == "1" and marca_buscar != auto["marca"].lower():
            continue
        elif opcion_filtro == "2" and estado_buscar != auto["estado"].lower():
            continue
        print(
            f"ID: {auto['id']} | Patente: {auto['patente']} | {auto['marca']} {auto['modelo']}"
        )
        print(f"Estado: {auto['estado']} | Precio: ${auto['precio']}")
        print("-" * 30)


##funciones que retornan valores. buscar el auto de 2 formas en nuestra lista de diccionarios
def buscar_auto():
    print("\n--- BUSCAR AUTO ---")
    print("1. Por ID | 2. Por Patente")
    opcion = input("Opcion: ")
    if opcion == "1":
        id_buscar = pedir_entero("ID: ")
        for auto in lista_autos:
            if auto["id"] == id_buscar:
                return auto
    elif opcion == "2":
        patente_buscar = input("Patente: ").upper().strip()
        for auto in lista_autos:
            if auto["patente"] == patente_buscar:
                return auto
    return None


def cambiar_estado_auto():
    auto = buscar_auto()
    if auto is None:
        print("No existe.")
        return
    print(f"Estado actual: {auto['estado']}")
    auto["estado"] = pedir_estado_valido()
    guardar_autos(lista_autos)
    print("Estado actualizado.")


def dar_de_baja_auto():
    auto = buscar_auto()
    if auto is None:
        print("No existe.")
        return
    confirmacion = input("Seguro? (S/N): ").upper()
    if confirmacion == "S":
        lista_autos.remove(auto)
        guardar_autos(lista_autos)
        print("Eliminado.")


def menu_autos():
    global lista_autos, siguiente_id_auto
    lista_autos = cargar_autos()
    if len(lista_autos) > 0:
        siguiente_id_auto = max(auto["id"] for auto in lista_autos) + 1
    else:
        siguiente_id_auto = 1

    while True:
        print("\n--- MENU AUTOS ---")
        print("1. Cargar | 2. Listar | 3. Buscar | 4. Estado | 5. Baja | 9. Volver")
        opcion = input("Opcion: ")
        if opcion == "1":
            cargar_auto_nuevo()
        elif opcion == "2":
            ver_listado_autos()
        elif opcion == "3":
            auto = buscar_auto()
            print(auto if auto else "No encontrado.")
        elif opcion == "4":
            cambiar_estado_auto()
        elif opcion == "5":
            dar_de_baja_auto()
        elif opcion == "9":
            break


# main_concesionaria()  # funcion principal, punto de entrada. como no tiene def y esta pegada al margen izq, es una
# orden de ejecucion, en el recorrido del codido fue recolectando la info. comienza desde aca a buscar donde se definio.
# def son solo declaraciones  que se guardan en memoria pero no se ejecutan

if __name__ == "__main__":
    print("=== EL PROGRAMA ESTA ARRANCANDO CORRECTAMENTE ===")
    menu_autos()
