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
    print(f"""
    Forma de pago:
        {Color.AZUL}1. {Color.RESET}Contado
        {Color.AZUL}2. {Color.RESET}Financiado
        {Color.AZUL}3. {Color.RESET}Parte de pago (con otro auto)
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
    print(f"""
    Estado del pago:
        {Color.AZUL}1. {Color.RESET}Cobrado
        {Color.AZUL}2. {Color.RESET}Pendiente
        {Color.AZUL}3. {Color.RESET}En cuotas
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
        # Validamos que los IDs recibidos por parámetro existan en la DB
        if _buscar_por_id("db/db_autos.json", id_auto) is None:
            print(
                f"{Color.ROJO}No existe un auto con ID {Color.RESET}{id_auto}.{Color.RESET}"
            )
            return None
        if (
            id_cliente is not None
            and _buscar_por_id("db/db_clientes.json", id_cliente) is None
        ):
            print(
                f"{Color.ROJO}No existe un cliente con ID {Color.RESET}{id_cliente}.{Color.RESET}"
            )
            return None
        if (
            id_vendedor is not None
            and _buscar_por_id("db/db_vendedores.json", id_vendedor) is None
        ):
            print(
                f"{Color.ROJO}No existe un vendedor con ID {Color.RESET}{id_vendedor}.{Color.RESET}"
            )
            return None
        id_ventas = _id_autoincremental("db/db_ventas.json")
        _limpiar_pantalla()
        print("""\n
    ═══════════════════════════════════════════════════
    CONCRETANDO VENTA DE RESERVA
    ═══════════════════════════════════════════════════
        """)
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
        cambiar_estado_auto(nueva_venta["id_auto"], "vendido")
        # _db_actualizar_dato("db/db_autos.json", id_auto, "estado", "vendido")
        print(f"\n{Color.VERDE}Venta registrada correctamente.{Color.RESET}")
        input(f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar...")
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
                print(f"\n{Color.VERDE}Venta registrada correctamente.{Color.RESET}")
                venta_registrada = nueva_venta
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )
                opcion = 0  # Volver al menú tras crear la venta
            case 0:
                pass
            case _:
                print(f"\n{Color.ROJO}Opción no válida.{Color.RESET}")
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )

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
                    print(f"\n{Color.ROJO}La lista de ventas esta vacia{Color.RESET}")
                    input(
                        f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                    )
                    return

                print("\nLista completa:\n")

                for datos in lectura:
                    print(f"""
    ----------------------------------------
    {Color.CYAN}ID: {Color.RESET}  {datos["id"]}
    {Color.CYAN}ID del auto:      {Color.RESET}  {datos["id_auto"]}
    {Color.CYAN}ID del cliente:   {Color.RESET}  {datos["id_cliente"]}
    {Color.CYAN}ID del vendedor:  {Color.RESET}  {datos["id_vendedor"]}
    {Color.CYAN}Fecha de venta:   {Color.RESET}  {datos["fecha_venta"]}
    {Color.CYAN}Precio final:     {Color.RESET}  ${datos["precio_final"]}
    {Color.CYAN}Forma de pago:    {Color.RESET}  {datos["forma_pago"]}
    {Color.CYAN}Estado de pago:   {Color.RESET}  {datos["estado_pago"]}
    ----------------------------------------
                    """)
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )
            case 0:
                pass
            case _:
                print(f"\n{Color.ROJO}Opción no válida.{Color.RESET}")
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )


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
                    print(f"\n{Color.ROJO}No hay autos registrados.{Color.RESET}")
                    input(
                        f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                    )
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
                            print(
                                f"\n{Color.ROJO}No existe ninguna venta registrada para ese auto.{Color.RESET}"
                            )
                        else:
                            print(f"""
    ----------------------------------------
    {Color.CYAN}ID de venta:      {Color.RESET}  {venta["id"]}
    {Color.CYAN}ID del auto:      {Color.RESET}  {venta["id_auto"]}
    {Color.CYAN}ID del cliente:   {Color.RESET}  {venta["id_cliente"]}
    {Color.CYAN}ID del vendedor:  {Color.RESET}  {venta["id_vendedor"]}
    {Color.CYAN}Fecha de venta:   {Color.RESET}  {venta["fecha_venta"]}
    {Color.CYAN}Precio final:     {Color.RESET}  {venta["precio_final"]}
    {Color.CYAN}Forma de pago:    {Color.RESET}  {venta["forma_pago"]}
    {Color.CYAN}Estado de pago:   {Color.RESET}  {venta["estado_pago"]}
    ----------------------------------------
                            """)
                # Si no se encuentra el auto, mostramos un mensaje
                if not encontrado:
                    print(
                        f"\n{Color.ROJO}No se encontró ningún auto con la patente: {Color.RESET}{patente}{Color.RESET}"
                    )

                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )

            case 2:  # Buscar por DNI
                _limpiar_pantalla()

                datos_clientes = _db_leer_datos("db/db_clientes.json")

                encontrado = False

                if not datos_clientes:
                    print(f"\n{Color.ROJO}No hay clientes registrados.{Color.RESET}")
                    input(
                        f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                    )
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
                                f"\n{Color.ROJO}No existe ninguna venta registrada para este cliente.{Color.RESET}"
                            )
                        else:
                            print(f"""
    ----------------------------------------
    {Color.AZUL}ID de venta:      {Color.RESET}  {venta["id"]}
    {Color.CYAN}ID del auto:      {Color.RESET}  {venta["id_auto"]}
    {Color.CYAN}ID del cliente:   {Color.RESET}  {venta["id_cliente"]}
    {Color.CYAN}ID del vendedor:  {Color.RESET}  {venta["id_vendedor"]}
    {Color.CYAN}Fecha de venta:   {Color.RESET}  {venta["fecha_venta"]}
    {Color.CYAN}Precio final:     {Color.RESET}  {venta["precio_final"]}
    {Color.CYAN}Forma de pago:    {Color.RESET}  {venta["forma_pago"]}
    {Color.CYAN}Estado de pago:   {Color.RESET}  {venta["estado_pago"]}
    ----------------------------------------
                            """)
                if not encontrado:
                    print(
                        f"\n{Color.ROJO}No se encontró ningún cliente con el DNI: {Color.RESET}{dni}{Color.RESET}"
                    )

                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )

            case 3:  # Buscar venta por DNI de vendedor
                _limpiar_pantalla()

                datos_vendedores = _db_leer_datos("db/db_vendedores.json")

                encontrado = False

                if not datos_vendedores:
                    print(f"\n{Color.ROJO}No hay vendedores registrados.{Color.RESET}")
                    input(
                        f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                    )
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
                                f"\n{Color.ROJO}No existe ninguna venta registrada por este vendedor.{Color.RESET}"
                            )
                        else:
                            for venta_vendedor in venta:
                                print(f"""
    ----------------------------------------
    {Color.CYAN}ID de venta:      {Color.RESET}  {venta_vendedor["id"]}
    {Color.CYAN}ID del auto:      {Color.RESET}  {venta_vendedor["id_auto"]}
    {Color.CYAN}ID del cliente:   {Color.RESET}  {venta_vendedor["id_cliente"]}
    {Color.CYAN}ID del vendedor:  {Color.RESET}  {venta_vendedor["id_vendedor"]}
    {Color.CYAN}Fecha de venta:   {Color.RESET}  {venta_vendedor["fecha_venta"]}
    {Color.CYAN}Precio final:     {Color.RESET}  {venta_vendedor["precio_final"]}
    {Color.CYAN}Forma de pago:    {Color.RESET}  {venta_vendedor["forma_pago"]}
    {Color.CYAN}Estado de pago:   {Color.RESET}  {venta_vendedor["estado_pago"]}
    ----------------------------------------
                                    """)

                if not encontrado:
                    print(
                        f"\n{Color.ROJO}No se encontró ningún vendedor con el DNI: {Color.RESET}{dni}{Color.RESET}"
                    )
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )

            case 0:
                pass
            case _:
                print(f"\n{Color.ROJO}Opción no válida.{Color.RESET}")
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )


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
                    print(
                        f"\n{Color.ROJO}No se encontró una venta con ese ID.{Color.RESET}"
                    )
                    input(
                        f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                    )
                    return

                print(f"""
    {Color.AZUL}Venta encontrada:{Color.RESET}
    ----------------------------------------
    {Color.CYAN}ID:         {Color.RESET}  {venta["id"]}
    {Color.CYAN}Auto:         {Color.RESET}  {venta["id_auto"]}
    {Color.CYAN}Cliente:      {Color.RESET}  {venta["id_cliente"]}
    {Color.CYAN}Vendedor:     {Color.RESET}  {venta["id_vendedor"]}
    {Color.CYAN}Precio final: ${Color.RESET}  {venta["precio_final"]}
    {Color.CYAN}Forma de pago: {Color.RESET}  {venta["forma_pago"]}
    {Color.CYAN}Estado actual: {Color.RESET}  {venta["estado_pago"]}
    ----------------------------------------
                 """)

                print("¿Confirma que quiere modificar esta venta? (s/n): ", end="")
                confirmacion = input().strip().lower()  # Confirmación del usuario

                if confirmacion == "n":
                    return
                elif confirmacion != "s":
                    print(f"\n{Color.ROJO}Opción inválida.{Color.RESET}")
                    input(
                        f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                    )
                    return

                venta["estado_pago"] = _seleccionar_estado_pago()

                # Actualizar el estado de la venta en el archivo JSON
                _db_actualizar_dato(
                    "db/db_ventas.json",
                    venta["id"],
                    "estado_pago",
                    venta["estado_pago"],
                )  # Archivo, ID de la venta, campo a actualizar, nuevo valor

                print(
                    f"\n{Color.VERDE}Estado de la venta actualizado correctamente.{Color.RESET}"
                )
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )
            case 0:
                pass
            case _:
                print(f"\n{Color.ROJO}Opción inválida.{Color.RESET}")
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )


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
                    print(f"\n{Color.ROJO}La venta no existe.{Color.RESET}")
                    input(
                        f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                    )
                    pass
                else:
                    _db_eliminar_valor("db/db_ventas.json", id_venta)
                    print(f"\n{Color.VERDE}Venta eliminada correctamente.{Color.RESET}")
                    input(
                        f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                    )
            case 0:
                pass
            case _:
                print(f"\n{Color.ROJO}Opción inválida.{Color.RESET}")
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )


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
    {Color.ROJO}0.{Color.RESET} Volver al menú principal.
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
                pass
            case _:
                print(f"{Color.ROJO}Opción inválida, vuelva a intentarlo.{Color.RESET}")
                input(
                    f"\nPresione {Color.AMARILLO}ENTER {Color.RESET}para continuar..."
                )


if __name__ == "__main__":
    menu_ventas()
