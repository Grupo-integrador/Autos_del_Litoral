# date, fecha de ingreso al stock, al importar date se crea con fecha real
import json
from datetime import date

from utils.dbUtils import (
    _db_actualizar_dato,
    _db_eliminar_valor,
)
from utils.idUtils import _buscar_por_id
from utils.validateUtils import Color, _input_int, _limpiar_pantalla

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
    print("""
    ═══════════════════════════════════════════════════
    🚗 CARGAR NUEVO AUTO
    ═══════════════════════════════════════════════════
    """)
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
    print(f"{Color.VERDE}Auto cargado con exito.{Color.RESET}")
    input(f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar...")
    siguiente_id_auto += 1  # suma 1 a la variable global


def ver_listado_autos():
    print("\n--- LISTADO DE AUTOS EN STOCK ---")
    print("""
    ═══════════════════════════════════════════════════
    🚗 LISTADO DE AUTOS EN STOCK
    ═══════════════════════════════════════════════════
    """)
    if not lista_autos:
        print(f"{Color.ROJO}No hay autos.{Color.RESET}")
        return
    print(f"""
    {Color.AZUL}Filtros:{Color.RESET}
    {Color.CYAN}0. {Color.RESET}Sin filtro
    {Color.CYAN}1. {Color.RESET}Por Marca
    {Color.CYAN}2. {Color.RESET}Por Estado
    """)
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
            f"""
    {Color.CYAN}ID: {Color.RESET}{auto["id"]}
    {Color.CYAN}Patente: {Color.RESET}{auto["patente"]} | {auto["marca"]} {auto["modelo"]}
    {Color.CYAN}Estado: {Color.RESET}{auto["estado"]}
    {Color.CYAN}Precio: {Color.RESET}${auto["precio"]}
    """
        )
        print("-" * 30)
    input(f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar...")


##funciones que retornan valores. buscar el auto de 2 formas en nuestra lista de diccionarios
def buscar_auto():
    print(f"""
    ═══════════════════════════════════════════════════
    🚗 BUSCAR AUTO
    ═══════════════════════════════════════════════════
    {Color.CYAN}1. {Color.RESET}Por ID
    {Color.CYAN}2. {Color.RESET}Por Patente
    """)
    opcion = input("Opcion: ")
    if opcion == "1":
        id_buscar = pedir_entero("ID: ")
        auto = _buscar_por_id("db/db_autos.json", id_buscar)
        if auto is not None:
            print(f"""
    {Color.AZUL}Auto encontrado:{Color.RESET}
    {Color.CYAN}id: {Color.RESET}{auto["id"]}
    {Color.CYAN}patente: {Color.RESET}{auto["patente"]}
    {Color.CYAN}marca: {Color.RESET}{auto["marca"]}
    {Color.CYAN}modelo: {Color.RESET}{auto["modelo"]}
    {Color.CYAN}año: {Color.RESET}{auto["anio"]}
    {Color.CYAN}kilometraje: {Color.RESET}{auto["kilometros"]}
    {Color.CYAN}precio: {Color.RESET}{auto["precio"]}
    {Color.CYAN}estado: {Color.RESET}{auto["estado"]}
    {Color.CYAN}fecha_ingreso: {Color.RESET}{auto["fecha_ingreso"]}
    """)
            input(f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar...")
            return auto
        else:
            print(f"{Color.ROJO}No existe auto con ID {Color.RESET}{id_buscar}.")
            input(f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar...")
            return None
    elif opcion == "2":
        patente_buscar = input("Patente: ").upper().strip()
        for auto in lista_autos:
            if auto["patente"] == patente_buscar:
                return auto
    return None


# Cambia el estado de un auto por su ID. Si no se proporciona un nuevo valor, se pide al usuario.
def cambiar_estado_auto(id_auto=None, nuevo_valor=None):
    # Verificamos si el ID del auto viene por parametros o se pide al usuario
    if id_auto is None:
        id_auto = _input_int("ID: ")

    # Busca el auto en la base de datos
    auto = _buscar_por_id("db/db_autos.json", id_auto)

    # Si el nuevo valor viene por parametro, se actualiza directamente
    if nuevo_valor is not None:
        _db_actualizar_dato("db/db_autos.json", id_auto, "estado", nuevo_valor)
        return

    # Si el nuevo valor no viene por parametro, se pide al usuario que lo ingrese y luego se actualiza
    if auto is not None:
        print(f"Estado actual: {auto['estado']}")
        auto["estado"] = pedir_estado_valido()
        _db_actualizar_dato("db/db_autos.json", id_auto, "estado", auto["estado"])
        print(f"{Color.VERDE}Estado actualizado.{Color.RESET}")
    else:
        print(f"{Color.ROJO}No existe.{Color.RESET}")


def dar_de_baja_auto():
    auto = buscar_auto()
    if auto is None:
        print(f"{Color.ROJO}No existe.{Color.RESET}")
        return
    confirmacion = input("Seguro? (S/N): ").upper()
    if confirmacion == "S":
        _db_eliminar_valor("db/db_autos.json", auto["id"])

        print(f"{Color.VERDE}Eliminado.{Color.RESET}")
        input(f"Presione {Color.AMARILLO}ENTER{Color.RESET} para continuar...")


def menu_autos():
    global lista_autos, siguiente_id_auto
    lista_autos = cargar_autos()
    if len(lista_autos) > 0:
        siguiente_id_auto = max(auto["id"] for auto in lista_autos) + 1
    else:
        siguiente_id_auto = 1

    while True:
        _limpiar_pantalla()
        print(f"""
    ═══════════════════════════════════════════════════
    🚗 AUTOS
    ═══════════════════════════════════════════════════
    {Color.CYAN}1. {Color.RESET}Cargar
    {Color.CYAN}2. {Color.RESET}Listar
    {Color.CYAN}3. {Color.RESET}Buscar
    {Color.CYAN}4. {Color.RESET}Estado
    {Color.CYAN}5. {Color.RESET}Baja
    {Color.ROJO}9. {Color.RESET}Volver
    """)
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
