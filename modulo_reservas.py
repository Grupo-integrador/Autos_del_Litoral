from datetime import datetime, timedelta

ESTADO_RESERVA_ACTIVA = "activa"
ESTADO_RESERVA_VENTA = "venta"
ESTADO_RESERVA_CANCELADA = "cancelada"


# funcion para agregar reservas mediante un diccionario a la lista de reservas
def registrar_nueva_reserva(lista_reservas):
    print("--- NUEVA RESERVA ---")

    numero_unico = ingresar_entero("Ingresar numero_unico: ")
    auto = input("Ingresar auto: ").lower()
    cliente = input("Ingresar cliente: ").lower()
    vendedor = input("Ingresar vendedor: ").lower()
    monto_reserva = ingresar_float("Ingresar monto_reserva: ")

    momento_actual = datetime.now()
    momento_limite = momento_actual + timedelta(days=30)  # fecha limite

    # Convertimos ambas a texto para guardarlas en el diccionario
    fecha_reserva_texto = momento_actual.strftime("%d-%m-%Y")
    fecha_limite_texto = momento_limite.strftime("%d-%m-%Y")

    id = 1
    if len(lista_reservas) > 0:
        ultima_reserva = lista_reservas[-1]
        id = ultima_reserva["id_key"] + 1

    nueva_reserva = {
        "id_key": id,
        "numero_unico": numero_unico,  # 345
        "auto": auto,  # fiat cronos - AD987CE
        "cliente": cliente,  # Carlos López
        "vendedor": vendedor,  # Pedro Martínez
        "monto_reserva": monto_reserva,  # 400000
        "fecha_reserva": fecha_reserva_texto,  # 25-05-2026
        "fecha_limite": fecha_limite_texto,  # 25-06-2026
        "estado": ESTADO_RESERVA_ACTIVA,
    }

    lista_reservas.append(nueva_reserva)
    print(f"¡Reserva guardada! Vence el: {fecha_limite_texto}")


# funcion para mostrar las reservas activas
def listar_reservas_activas(lista_reservas):
    if len(lista_reservas) == 0:
        print("No hay reservas registradas")
        return

    for nueva_reserva in lista_reservas:
        if nueva_reserva["estado"] == ESTADO_RESERVA_ACTIVA:
            print("-" * 20)
            print(f"ID: {nueva_reserva['id_key']}")
            print(f"Número único: {nueva_reserva['numero_unico']}")
            print(f"Auto: {nueva_reserva['auto']}")
            print(f"Cliente: {nueva_reserva['cliente']}")
            print(f"Vendedor: {nueva_reserva['vendedor']}")
            print(f"Monto reserva: ${nueva_reserva['monto_reserva']}")
            print(f"Fecha reserva: {nueva_reserva['fecha_reserva']}")
            print(f"Fecha límite: {nueva_reserva['fecha_limite']}")
            print(f"Estado: {nueva_reserva['estado']}")
            print("-" * 20)
        else:
            print("No hay reservas activas")


# funcion para buscar reservas
def buscar_reservas(lista_reservas):

    print("1. Buscar por auto")
    print("2. Buscar por cliente")
    print("3. Buscar por vendedor")

    opcion = ingresar_entero("Opcion: ")

    match opcion:
        case 1:
            auto = input("Ingrese auto: ")
            for nueva_reserva in lista_reservas:
                if nueva_reserva["auto"].lower() == auto.lower():
                    print(nueva_reserva)
                    return
            print("No se encontró una reserva para el auto especificado.")
            return
        case 2:
            cliente = input("Ingrese cliente: ").lower()
            for nueva_reserva in lista_reservas:
                if nueva_reserva["cliente"].lower() == cliente.lower():
                    print(nueva_reserva)
                    return
            print("No se encontró una reserva para el cliente especificado.")
            return

        case 3:
            vendedor = input("Ingrese vendedor: ").lower()
            for nueva_reserva in lista_reservas:
                if nueva_reserva["vendedor"].lower() == vendedor.lower():
                    print(nueva_reserva)
                    return
            print("No se encontró una reserva para el vendedor especificado.")
            return


# funcion para concretar ventas
def concretar_venta(lista_reservas):
    print("1. Concretar venta por auto")
    print("2. Concretar venta por cliente")
    print("3. Concretar venta por vendedor")

    opcion = ingresar_entero("Opcion: ")

    match opcion:
        case 1:
            auto = input("Ingrese auto: ")
            for nueva_reserva in lista_reservas:
                if nueva_reserva["auto"].lower() == auto.lower():
                    nueva_reserva["monto_reserva"] += ingresar_float(
                        "Ingresar monto a saldar: "
                    )
                    nueva_reserva["estado"] = ESTADO_RESERVA_VENTA
                    print("¡Venta concretada y monto actualizado exitosamente!")

        case 2:
            cliente = input("Ingrese cliente: ").lower()
            for nueva_reserva in lista_reservas:
                if nueva_reserva["cliente"].lower() == cliente.lower():
                    nueva_reserva["monto_reserva"] += ingresar_float(
                        "Ingresar monto a saldar: "
                    )
                    nueva_reserva["estado"] = ESTADO_RESERVA_VENTA
                    print("¡Venta concretada y monto actualizado exitosamente!")

        case 3:
            vendedor = input("Ingrese vendedor: ").lower()
            for nueva_reserva in lista_reservas:
                if nueva_reserva["vendedor"].lower() == vendedor.lower():
                    nueva_reserva["monto_reserva"] += ingresar_float(
                        "Ingresar monto a saldar: "
                    )
                    nueva_reserva["estado"] = ESTADO_RESERVA_VENTA
                    print("¡Venta concretada y monto actualizado exitosamente!")


# funcion para cancelar reservas
def cancelar_reserva(lista_reservas):
    print("1. Cancelar venta por auto")
    print("2. Cancelar venta por cliente")
    print("3. Cancelar venta por vendedor")

    opcion = ingresar_entero("Opcion: ")

    match opcion:
        case 1:
            auto = input("Ingrese auto: ")
            for nueva_reserva in lista_reservas:
                if nueva_reserva["auto"].lower() == auto.lower():
                    nueva_reserva["estado"] = ESTADO_RESERVA_CANCELADA
                    print("¡Reserva cancelada exitosamente!")
        case 2:
            cliente = input("Ingrese cliente: ").lower()
            for nueva_reserva in lista_reservas:
                if nueva_reserva["cliente"].lower() == cliente.lower():
                    nueva_reserva["estado"] = ESTADO_RESERVA_CANCELADA
                    print("¡Reserva cancelada exitosamente!")

        case 3:
            vendedor = input("Ingrese vendedor: ").lower()
            for nueva_reserva in lista_reservas:
                if nueva_reserva["vendedor"].lower() == vendedor.lower():
                    nueva_reserva["estado"] = ESTADO_RESERVA_CANCELADA
                    print("¡Reserva cancelada exitosamente!")


# funcion validacion datos entrada
def ingresar_entero(msj: str) -> int:
    a_retornar = input(msj)

    while not a_retornar.isnumeric():
        print("El valor ingresado no es numerico!")
        a_retornar = input(msj)

    return int(a_retornar)


def ingresar_float(msj: str) -> float:
    while True:
        try:
            return float(input(msj))
        except ValueError:
            print("El valor ingresado no es un número válido.")


# Declaramos los colores al principio (fuera de la función o al inicio de tu script)
class Color:
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


def main_reservas():
    # lista
    lista_reservas = []

    opcion = -1

    while opcion != 0:
        print("\n")
        # Pintamos el título principal de color Cyan
        print(f"{Color.CYAN}=== RESERVAS ==={Color.RESET}")

        # Pintamos los números de las opciones en Azul para que resalten
        print(f"{Color.AZUL}1.{Color.RESET} Registrar una nueva reserva ")
        print(f"{Color.AZUL}2.{Color.RESET} Listar reservas activas ")
        print(f"{Color.AZUL}3.{Color.RESET} Buscar reservas ")
        print(f"{Color.AZUL}4.{Color.RESET} Concretar venta ")
        print(f"{Color.AZUL}5.{Color.RESET} Cancelar reserva")
        print(f"{Color.ROJO}0.{Color.RESET} Salir")

        print(f"{Color.AMARILLO}Elegi una opcion:{Color.RESET}")
        opcion = int(input())

        match opcion:
            case 1:
                registrar_nueva_reserva(lista_reservas)  # parametro
            case 2:
                listar_reservas_activas(lista_reservas)
            case 3:
                buscar_reservas(lista_reservas)
            case 4:
                concretar_venta(lista_reservas)
            case 5:
                cancelar_reserva(lista_reservas)

            case 0:
                print(f"\n{Color.VERDE}*Usted salio del programa*{Color.RESET}")
                break
            case _:  # como el default: en c
                # Mensaje de error en Rojo
                print(f"{Color.ROJO}Opción inválida, vuelve a intentarlo{Color.RESET}")


# main_reservas()

if __name__ == "__main__":
    main_reservas()
