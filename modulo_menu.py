from modulo_autos import menu_autos
from modulo_clientes import menu_clientes
from modulo_reservas import main_reservas
from modulo_vendedores import menu_vendedores
from modulo_ventas import menu_ventas
from modulo_vendedores import menu_vendedores
from utils.validateUtils import _input_int


def menu_principal():

    while True:
        _limpiar_pantalla()
        print(f"""
    ═══════════════════════════════════════════════════
    🚗 AUTOS DEL LITORAL — Sistema v1.0
    ═══════════════════════════════════════════════════
    {Color.CYAN}1. {Color.RESET}Autos en stock
    {Color.CYAN}2. {Color.RESET}Clientes
    {Color.CYAN}3. {Color.RESET}Ventas
    {Color.CYAN}4. {Color.RESET}Reservas
    {Color.CYAN}5. {Color.RESET}Vendedores
    {Color.ROJO}0. {Color.RESET}Salir del programa

    ¿Qué querés hacer?
            """)

        opcion = _input_int("Seleccione una opcion: ")

        match opcion:
            case 1:
                menu_autos()
            case 2:
                menu_clientes()
            case 3:
                menu_ventas()
            case 4:
                main_reservas()
            case 5:
                menu_vendedores()
            case 0:
                print(f"""
    ═══════════════════════════════════════════════════
                    {Color.AMARILLO}Saliendo del programa{Color.RESET}
    ═══════════════════════════════════════════════════
    """)
                break
            case _:
                print("Opción inválida, vuelva a intentarlo.\n")


menu_principal()
