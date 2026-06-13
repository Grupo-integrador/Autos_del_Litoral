# 💰 3. Las ventas
# Cuando un auto se vende, hay que dejarlo registrado. Una venta conecta un auto, un cliente y un
# vendedor. Necesito:
# • [x] Registrar una venta nueva (qué auto, qué cliente, qué vendedor, qué día, a qué precio).
# • [x] Ver todas las ventas hechas.
# • [] Buscar una venta por patente del auto, por DNI del cliente, o por vendedor.
# • [] Modificar el estado del pago si se vendió en cuotas.
# • [] Eliminar una venta si se anula la operación (rara vez, pero pasa).
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

from utils.dbUtils import _db_inyectar_datos, _db_leer_datos
from utils.idUtils import (
    _buscar_venta_por_id_modulo,
    _buscar_ventas_por_id_modulo,
    _id_autoincremental,
)
from utils.validateUtils import Color, _input_int, _input_str, _limpiar_pantalla


# Registrar una venta nueva
def registrar_venta():
    # TODO:
    # ⚠️ Importante: cuando se registra una venta, el auto tiene que pasar automáticamente a
    # estado "vendido". Yo no me tengo que acordar de cambiarlo.

    opcion = -1
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

                # print(ultimo_dato["id"])
                # TODO:
                # TRAER DATOS DE OTROS MODULOS:
                # Buscar en el modulo de Autos
                # Buscar en el modulo de Clientes
                # Buscar en el modulo de Vendedor
                nueva_venta = {
                    "id": id_ventas,
                    "id_auto": _input_int("Agregue el ID del auto: "),
                    "id_cliente": _input_int("Agregue el ID del cliente: "),
                    "id_vendedor": _input_int("Agregue el ID del vendedor: "),
                    "fecha_venta": str(date.today()),
                    "precio_final": f"${_input_int('Agregue el precio final: ')}",
                    "forma_pago": input("Agregue la forma de pago: "),
                    "estado_pago": input("Agregue el estado del pago: "),
                }
                _db_inyectar_datos("db/db_ventas.json", nueva_venta)
                print("\nVenta registrada correctamente.")
                input("\nPresione Enter para continuar...")
            case 0:
                pass
            case _:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")


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
    Precio final: {datos["precio_final"]}
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
    pass


# Eliminar una venta si se anula la operación (rara vez, pero pasa).
def eliminar_venta():
    pass


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
                print("Se modifico el estado del pago")
            case 5:
                print("Se elimino una venta")
            case 0:
                print("")
            case _:
                print("Opción inválida, vuelva a intentarlo.\n")
                input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    menu_ventas()
