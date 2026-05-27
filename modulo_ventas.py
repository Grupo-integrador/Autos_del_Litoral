# 💰 3. Las ventas
# Cuando un auto se vende, hay que dejarlo registrado. Una venta conecta un auto, un cliente y un
# vendedor. Necesito:
# • Registrar una venta nueva (qué auto, qué cliente, qué vendedor, qué día, a qué precio).
# • Ver todas las ventas hechas.
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


import json
from datetime import date

from utils.dbUtils import _db_inyectar_datos, _db_leer_datos
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
             2. Ver lista de ventas.
             0. Volver al menu de VENTAS.
            """)

        opcion = _input_int("Seleccione una opcion: ")

        match opcion:
            case 1:
                # TODO:
                # TRAER DATOS DE OTROS MODULOS:
                # Buscar en el modulo de Autos
                # Buscar en el modulo de Clientes
                # Buscar en el modulo de Vendedor
                nueva_venta = {
                    "fecha_venta": str(date.today()),
                    "precio_final": int(input("Agregue el precio final: ")),
                    "forma_pago": input("Agregue la forma de pago: "),
                    "estado_pago": input("Agregue el estado del pago: "),
                }
                _db_inyectar_datos("db/db_ventas.json", nueva_venta)

            case 2:
                lectura = _db_leer_datos("db/db_ventas.json")
                print(json.dumps(lectura, indent=4))
            case 0:
                print("Volviendo...")
            case _:
                print("Opción no válida.")


# Ver todas las ventas hechas
def ventas():
    pass


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

        match opcion:
            case 0:
                print("\n*Usted salio del programa*")
            case 1:
                registrar_venta()
            case 2:
                print("Todas las ventas...")
            case 3:
                print("Venta por Patente, DNI, Vendedor")
            case 4:
                print("Se modifico el estado del pago")
            case 5:
                print("Se elimino una venta")
            case _:
                print("Opción inválida, vuelva a intentarlo.\n")


menu_ventas()
