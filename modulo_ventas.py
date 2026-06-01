# 💰 3. Las ventas
# Cuando un auto se vende, hay que dejarlo registrado. Una venta conecta un auto, un cliente y un
# vendedor. Necesito:
# • [x] Registrar una venta nueva (qué auto, qué cliente, qué vendedor, qué día, a qué precio).
# • [x] Ver todas las ventas hechas.
# • Buscar una venta por patente del auto, por DNI del cliente, o por vendedor.
# • Modificar el estado del pago si se vendió en cuotas.
# • Eliminar una venta si se anula la operación (rara vez, pero pasa).
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
from utils.idUtils import _id_autoincremental
from utils.validateUtils import _input_int


# Registrar una venta nueva
def registrar_venta():
    # TODO:
    # ⚠️ Importante: cuando se registra una venta, el auto tiene que pasar automáticamente a
    # estado "vendido". Yo no me tengo que acordar de cambiarlo.

    opcion = -1

    while opcion != 0:
        print("""
    ═══════════════════════════════════════════════════
    💰 REGISTRAR VENTA
    ═══════════════════════════════════════════════════
    1. Crear venta.
    0. Volver al menu de VENTAS.
            """)

        opcion = _input_int("Seleccione una opcion: ")
        print("-" * 20)

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
                print("-" * 20)
            case 0:
                pass
            case _:
                print("Opción no válida.")


# Ver todas las ventas hechas
def ventas():
    opcion = -1

    while opcion != 0:
        print("""
    ═══════════════════════════════════════════════════
    💰 VER VENTAS
    ═══════════════════════════════════════════════════
    1. Ver lista de todas las ventas hechas.
    0. Volver al menu de VENTAS.
            """)

        opcion = _input_int("Seleccione una opcion: ")

        match opcion:
            case 1:
                lectura = _db_leer_datos("db/db_ventas.json")

                if not lectura:
                    print("\nLa lista de ventas esta vacia")
                    return print("-" * 20)

                print("Lista completa:\n")

                for datos in lectura:
                    print(f"\t ID: {datos['id']}")
                    print(f"\t ID del auto: {datos['id_auto']}")
                    print(f"\t ID del cliente: {datos['id_cliente']}")
                    print(f"\t ID del vendedor: {datos['id_vendedor']}")
                    print(f"\t Fecha de venta: {datos['fecha_venta']}")
                    print(f"\t Precio final: {datos['precio_final']}")
                    print(f"\t Forma de pago: {datos['forma_pago']}")
                    print(f"\t Estado de pago: {datos['estado_pago']}")
                    print(f"\t{'-' * 20}\n")
                # print(json.dumps(lectura, indent=4))
            case 0:
                print("-" * 20)
            case _:
                print("Opción no válida.")


# Buscar una venta por patente del auto, por DNI del cliente, o por vendedor
def buscar_venta():
    pass


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
        print("""
    ═══════════════════════════════════════════════════
    💰 VENTAS
    ═══════════════════════════════════════════════════
    1. Registrar una venta nueva.
    2. Ver todas las ventas hechas.
    3. Buscar una venta.
    4. Modificar el estado del pago.
    5. Eliminar una venta.
    0. Salir.
            """)

        opcion = _input_int("Seleccione una opcion: ")
        print("-" * 20)
        match opcion:
            case 1:
                registrar_venta()
            case 2:
                ventas()
            case 3:
                print("Venta por Patente, DNI, Vendedor")
            case 4:
                print("Se modifico el estado del pago")
            case 5:
                print("Se elimino una venta")
            case 0:
                print("\n*Usted salio del programa*")
            case _:
                print("Opción inválida, vuelva a intentarlo.\n")


if __name__ == "__main__":
    menu_ventas()
