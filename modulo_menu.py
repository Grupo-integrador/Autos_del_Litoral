from modulo_autos import main_concesionaria
from modulo_clientes import menu_clientes
from modulo_reservas import main_reservas
from modulo_ventas import menu_ventas
from utils.validateUtils import _input_int


def menu_principal():

    while True:
        print("""
    ═══════════════════════════════════════════════════
    🚗 AUTOS DEL LITORAL — Sistema v1.0
    ═══════════════════════════════════════════════════
    1. Autos en stock
    2. Clientes
    3. Ventas
    4. Reservas
    5. Vendedores
    0. Salir

    ¿Qué querés hacer?
            """)

        opcion = _input_int("Seleccione una opcion: ")

        match opcion:
            case 1:
                main_concesionaria()
            case 2:
                menu_clientes()
            case 3:
                menu_ventas()
            case 4:
                main_reservas()
            case 5:
                print("Modulo Vendedores")
            case 0:
                print("Saliendo del programa")
                break
            case _:
                print("Opción inválida, vuelva a intentarlo.\n")


menu_principal()
