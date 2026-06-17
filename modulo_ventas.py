# 💰 3. Las ventas
# Cuando un auto se vende, hay que dejarlo registrado. Una venta conecta un auto, un cliente y un
# vendedor. Necesito:
# • [x] Registrar una venta nueva (qué auto, qué cliente, qué vendedor, qué día, a qué precio).
# • [x] Ver todas las ventas hechas.
# • [x] Buscar una venta por patente del auto, por DNI del cliente, o por vendedor.
# • [x] Modificar el estado del pago si se vendió en cuotas.
# • [x] Eliminar una venta si se anula la operación (rara vez, pero pasa).
# De cada venta quiero guardar:
# • Un número (único).
# • A qué auto corresponde.
# • A qué cliente corresponde.
# • A qué vendedor corresponde.
# • Fecha de la venta.
# • Precio final acordado (puede no ser el precio de lista — siempre se negocia).
# • Forma de pago (contado, financiado, parte de pago con otro auto).
# • Estado del pago (cobrado, pendiente, en cuotas).

from datetime import date

from modulo_autos import cambiar_estado_auto
from utils.dbUtils import (
    _db_actualizar_dato,
    _db_eliminar_valor,
    _db_inyectar_datos,
    _db_leer_datos,
)
from utils.idUtils import (
    _buscar_por_id,
    _buscar_por_id_validado,
    _buscar_venta_por_id_modulo,
    _buscar_ventas_por_id_modulo,
    _id_autoincremental,
)
from utils.validateUtils import Color, _input_int, _input_str, _limpiar_pantalla

# ====================================================
#                       UTILIDADES
# ====================================================


# Función para seleccionar la forma de pago
def _seleccionar_forma_pago():
    print("""
    Forma de pago:
        1. Contado
        2. Financiado
        3. Parte de pago (con otro auto)
            """)

    opcion = _input_int("Seleccione una opcion ")

    match opcion:
        case 1:
            return "contado"
        case 2:
            return "financiado"
        case 3:
            return "parte de pago con otro auto"
        case _:
            print("Opción no válida.")
            return _seleccionar_forma_pago()


# Función para seleccionar el estado del pago
def _seleccionar_estado_pago():
    print("""
    Estado del pago:
        1. Cobrado
        2. Pendiente
        3. En cuotas
            """)

    opcion = _input_int("Seleccione una opcion ")

    match opcion:
        case 1:
            return "cobrado"
        case 2:
            return "pendiente"
        case 3:
            return "en cuotas"
        case _:
            print("Opción no válida.")
            return _seleccionar_estado_pago()


# ====================================================


# Registrar una venta nueva
def registrar_venta(id_auto=None, id_cliente=None, id_vendedor=None, precio_final=None):
    # Si se llama con argumentos (ej. desde concretar_venta), se registra directamente sin menú
    if id_auto is not None:
        id_ventas = _id_autoincremental("db/db_ventas.json")
        _limpiar_pantalla()
        print("\n=== CONCRETANDO VENTA DE RESERVA ===")
        nueva_venta = {
            "id": id_ventas,
            "id_auto": id_auto,
            "id_cliente": id_cliente
            if id_cliente is not None
            else _input_int("Agregue el ID del cliente: "),
            "id_vendedor": id_vendedor
            if id_vendedor is not None
            else _input_int("Agregue el ID del vendedor: "),
            "fecha_venta": str(date.today()),
            "precio_final": precio_final
            if precio_final is not None
            else _input_int("Agregue el precio final: "),
            "forma_pago": _seleccionar_forma_pago(),
            "estado_pago": _seleccionar_estado_pago(),
        }
        _db_inyectar_datos("db/db_ventas.json", nueva_venta)
        _db_actualizar_dato("db/db_autos.json", id_auto, "estado", "vendido")
        print("\nVenta registrada correctamente.")
        input("\nPresione Enter para continuar...")
        return nueva_venta

    opcion = -1
    venta_registrada = None

    while opcion != 0:
        _limpiar_pantalla()
        print(f"""
    ═══════════════════════════════════════════════════
    💰 REGISTRAR VENTA
    ═══════════════════════════════════════════════════
    {Color.AZUL}1. {Color.RESET}Crear venta.
    {Color.ROJO}0. {Color.RESET}Volver al menu de VENTAS.
            """)

        opcion = _input_int("Seleccione una opcion: ")
        match opcion:
            case 1:
                id_ventas = _id_autoincremental("db/db_ventas.json")

                _limpiar_pantalla()
                nueva_venta = {
                    "id": id_ventas,
                    #
                    "id_auto": _buscar_por_id_validado(
                        "db/db_autos.json", "Agregue el ID del auto: "
                    )["id"],
                    #
                    "id_cliente": _buscar_por_id_validado(
                        "db/db_clientes.json", "Agregue el ID del cliente: "
                    )["id"],
                    #
                    "id_vendedor": _buscar_por_id_validado(
                        "db/db_vendedores.json", "Agregue el ID del vendedor: "
                    )["id"],
                    #
                    "fecha_venta": str(date.today()),
                    #
                    "precio_final": _input_int("Agregue el precio final: "),
                    #
                    "forma_pago": _seleccionar_forma_pago(),
                    "estado_pago": _seleccionar_estado_pago(),
                }
                # Se inyectan los datos en la base de ventas
                _db_inyectar_datos("db/db_ventas.json", nueva_venta)
                # Luego se cambia el estado del auto a "vendido"
                cambiar_estado_auto(nueva_venta["id_auto"], "vendido")
                print("\nVenta registrada correctamente.")
                venta_registrada = nueva_venta
                input("\nPresione Enter para continuar...")
                opcion = 0  # Volver al menú tras crear la venta
            case 0:
                pass
            case _:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")

    return venta_registrada


# Ver todas las ventas hechas
def ventas():
    opcion = -1
    while opcion != 0:
        _limpiar_pantalla()
        print(f"""
    ═══════════════════════════════════════════════════
    💰 VER VENTAS
    ═══════════════════════════════════════════════════
    {Color.AZUL}1. {Color.RESET}Ver lista de todas las ventas hechas.
    {Color.ROJO}0. {Color.RESET}Volver al menu de VENTAS.
            """)

        opcion = _input_int("Seleccione una opcion: ")
        match opcion:
            case 1:
                _limpiar_pantalla()
                lectura = _db_leer_datos("db/db_ventas.json")

                if not lectura:
                    print("\nLa lista de ventas esta vacia")
                    return print("-" * 20)

                print("\nLista completa:\n")

                for datos in lectura:
                    print(f"""
    ----------------------------------------
    ID: {datos["id"]}
    ID del auto: {datos["id_auto"]}
    ID del cliente: {datos["id_cliente"]}
    ID del vendedor: {datos["id_vendedor"]}
    Fecha de venta: {datos["fecha_venta"]}
    Precio final: ${datos["precio_final"]}
    Forma de pago: {datos["forma_pago"]}
    Estado de pago: {datos["estado_pago"]}
    ----------------------------------------
                    """)
                input("\nPresione Enter para continuar...")
            case 0:
                pass
            case _:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")


# Buscar una venta por patente del auto, por DNI del cliente, o por vendedor
def buscar_venta():
    opcion = -1
    while opcion != 0:
        _limpiar_pantalla()
        print(f"""
    ═══════════════════════════════════════════════════
    💰 BUSCAR UNA VENTA
    ═══════════════════════════════════════════════════
    {Color.AZUL}1. {Color.RESET}Por Patente.
    {Color.AZUL}2. {Color.RESET}Por DNI.
    {Color.AZUL}3. {Color.RESET}Por Vendedor.
    {Color.ROJO}0. {Color.RESET}Volver al menu de VENTAS.
            """)

        opcion = _input_int("Seleccione una opcion: ")
        match opcion:
            case 1:  # Buscar por PATENTE
                _limpiar_pantalla()
                # Traemos los datos de la DB de autos
                datos_autos = _db_leer_datos("db/db_autos.json")

                encontrado = False  # Si no se encuentra el auto, se mantiene en False

                # Si no hay autos registrados, se muestra un mensaje y se retorna
                if not datos_autos:
                    print("No hay autos registrados.")
                    input("Presione Enter para continuar...")
                    return

                patente = _input_str("Ingrese la patente: ").upper()

                # Verificamos si el auto existe en la lista de autos mediante la patente
                for dato_patente in datos_autos:
                    if dato_patente["patente"] == patente:
                        encontrado = True

                        # Si se encuentra el auto, buscamos la venta correspondiente
                        venta = _buscar_venta_por_id_modulo(
                            dato_patente["id"], "db/db_ventas.json", "id_auto"
                        )
                        # Si no se encuentra la venta, mostramos un mensaje, sino mostramos los datos de la venta
                        if venta is None:
                            print("No existe ninguna venta registrada para ese auto.")
                        else:
                            print(f"""
    ----------------------------------------
    ID de venta:      {venta["id"]}
    ID del auto:      {venta["id_auto"]}
    ID del cliente:   {venta["id_cliente"]}
    ID del vendedor:  {venta["id_vendedor"]}
    Fecha de venta:   {venta["fecha_venta"]}
    Precio final:     {venta["precio_final"]}
    Forma de pago:    {venta["forma_pago"]}
    Estado de pago:   {venta["estado_pago"]}
    ----------------------------------------
                            """)
                # Si no se encuentra el auto, mostramos un mensaje
                if not encontrado:
                    print(f"No se encontró ningún auto con la patente: {patente}")

                input("\nPresione Enter para continuar...")

            case 2:  # Buscar por DNI
                _limpiar_pantalla()

                datos_clientes = _db_leer_datos("db/db_clientes.json")

                encontrado = False

                if not datos_clientes:
                    print("No hay clientes registrados.")
                    input("\nPresione Enter para continuar...")
                    return

                dni = _input_str("Ingrese el DNI: ")
                for cliente in datos_clientes:
                    if cliente["dni"] == dni:
                        print(f"Cliente encontrado: {cliente['nombre_completo']}")
                        encontrado = True

                        venta = _buscar_venta_por_id_modulo(
                            cliente["id"], "db/db_ventas.json", "id_cliente"
                        )
                        if venta is None:
                            print(
                                "No existe ninguna venta registrada para este cliente."
                            )
                        else:
                            print(f"""
    ----------------------------------------
    ID de venta:      {venta["id"]}
    ID del auto:      {venta["id_auto"]}
    ID del cliente:   {venta["id_cliente"]}
    ID del vendedor:  {venta["id_vendedor"]}
    Fecha de venta:   {venta["fecha_venta"]}
    Precio final:     {venta["precio_final"]}
    Forma de pago:    {venta["forma_pago"]}
    Estado de pago:   {venta["estado_pago"]}
    ----------------------------------------
                            """)
                if not encontrado:
                    print(f"No se encontró ningún cliente con el DNI: {dni}")

                input("\nPresione Enter para continuar...")

            case 3:  # Buscar venta por DNI de vendedor
                _limpiar_pantalla()

                datos_vendedores = _db_leer_datos("db/db_vendedores.json")

                encontrado = False

                if not datos_vendedores:
                    print("No hay vendedores registrados.")
                    input("\nPresione Enter para continuar...")
                    return

                dni = _input_str("Ingrese el DNI del vendedor: ")

                for vendedor in datos_vendedores:
                    if vendedor["dni"] == dni:
                        encontrado = True

                        venta = _buscar_ventas_por_id_modulo(
                            vendedor["id"], "db/db_ventas.json", "id_vendedor"
                        )
                        if venta is None:
                            print(
                                "No existe ninguna venta registrada por este vendedor."
                            )
                        else:
                            for venta_vendedor in venta:
                                print(f"""
    ----------------------------------------
    ID de venta:      {venta_vendedor["id"]}
    ID del auto:      {venta_vendedor["id_auto"]}
    ID del cliente:   {venta_vendedor["id_cliente"]}
    ID del vendedor:  {venta_vendedor["id_vendedor"]}
    Fecha de venta:   {venta_vendedor["fecha_venta"]}
    Precio final:     {venta_vendedor["precio_final"]}
    Forma de pago:    {venta_vendedor["forma_pago"]}
    Estado de pago:   {venta_vendedor["estado_pago"]}
    ----------------------------------------
                                    """)

                if not encontrado:
                    print(f"No se encontró ningún vendedor con el DNI: {dni}")

                input("\nPresione Enter para continuar...")

            case 0:
                pass
            case _:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")


# Modificar el estado del pago si se vendió en cuotas.
def cambiar_estado_de_venta():

    opcion = -1
    while opcion != 0:
        _limpiar_pantalla()
        print(f"""
    ═══════════════════════════════════════════════════
    💰 MODIFICAR ESTADO DE PAGO
    ═══════════════════════════════════════════════════
    {Color.AZUL}1. {Color.RESET}Cambiar estado de pago de una venta.
    {Color.ROJO}0. {Color.RESET}Volver al menu de VENTAS.
            """)

        opcion = _input_int("Seleccione una opción: ")
        match opcion:
            case 1:
                id_venta = _input_int("\nIngrese el ID de la venta: ")
                venta = _buscar_por_id("db/db_ventas.json", id_venta)

                if not venta:
                    print("No se encontró una venta con ese ID.")
                    input("\nPresione Enter para continuar...")
                    return

                print(f"""
    Venta encontrada:
    ----------------------------------------
    ID:           {venta["id"]}
    Auto:         {venta["id_auto"]}
    Cliente:      {venta["id_cliente"]}
    Vendedor:     {venta["id_vendedor"]}
    Precio final: ${venta["precio_final"]}
    Forma de pago:{venta["forma_pago"]}
    Estado actual:{venta["estado_pago"]}
    ----------------------------------------
                 """)

                print("¿Confirma que quiere modificar esta venta? (s/n): ", end="")
                confirmacion = input().strip().lower()  # Confirmación del usuario

                if confirmacion == "n":
                    return
                elif confirmacion != "s":
                    print("\nOpción inválida.")
                    input("\nPresione Enter para continuar...")
                    return

                venta["estado_pago"] = _seleccionar_estado_pago()

                # Actualizar el estado de la venta en el archivo JSON
                _db_actualizar_dato(
                    "db/db_ventas.json",
                    venta["id"],
                    "estado_pago",
                    venta["estado_pago"],
                )  # Archivo, ID de la venta, campo a actualizar, nuevo valor

                print("\nEstado de la venta actualizado correctamente.")
                input("Presione Enter para continuar...")
            case 0:
                pass
            case _:
                print("\nOpción inválida.")
                input("\nPresione Enter para continuar...")


# Eliminar una venta si se anula la operación (rara vez, pero pasa).
def eliminar_venta():

    opcion = -1
    while opcion != 0:
        _limpiar_pantalla()
        print(f"""
    ═══════════════════════════════════════════════════
    💰 ELIMINAR VENTA
    ═══════════════════════════════════════════════════
    {Color.AZUL}1. {Color.RESET}Eliminar una venta.
    {Color.ROJO}0. {Color.RESET}Volver al menu de VENTAS.
            """)

        opcion = _input_int("Seleccione una opción: ")

        match opcion:
            case 1:
                id_venta = _input_int("Ingrese el ID de la venta a eliminar: ")

                # Verificamos que exista la venta
                # Si no existe, mostramos un mensaje de error y volvemos al menú
                if not _buscar_por_id("db/db_ventas.json", id_venta):
                    print("\nLa venta no existe.")
                    input("Presione Enter para continuar...")
                    pass
                else:
                    _db_eliminar_valor("db/db_ventas.json", id_venta)
                    print("\nVenta eliminada correctamente.")
                    input("Presione Enter para continuar...")
            case 0:
                pass
            case _:
                print("\nOpción inválida.")
                input("\nPresione Enter para continuar...")


# Menu principal de VENTAS
def menu_ventas():

    opcion = -1
    while opcion != 0:
        _limpiar_pantalla()
        print(f"""
    ═══════════════════════════════════════════════════
    💰 VENTAS
    ═══════════════════════════════════════════════════
    {Color.AZUL}1.{Color.RESET} Registrar una venta nueva.
    {Color.AZUL}2.{Color.RESET} Ver todas las ventas hechas.
    {Color.AZUL}3.{Color.RESET} Buscar una venta.
    {Color.AZUL}4.{Color.RESET} Modificar el estado del pago.
    {Color.AZUL}5.{Color.RESET} Eliminar una venta.
    {Color.ROJO}0.{Color.RESET} Salir al menu principal.
            """)

        opcion = _input_int("Seleccione una opcion: ")
        match opcion:
            case 1:
                registrar_venta()
            case 2:
                ventas()
            case 3:
                buscar_venta()
            case 4:
                cambiar_estado_de_venta()
            case 5:
                eliminar_venta()
            case 0:
                print("")
            case _:
                print("Opción inválida, vuelva a intentarlo.\n")
                input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    menu_ventas()
