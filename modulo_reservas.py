import json
from datetime import date, timedelta
from utils.validateUtils import _input_int, Color
#from modulo_autos

ESTADO_RESERVA_ACTIVA = "activa"
ESTADO_RESERVA_VENTA = "concretada"
ESTADO_RESERVA_CANCELADA = "cancelada"


# funcion para agregar reservas mediante un diccionario a la lista de reservas
def registrar_nueva_reserva(lista_reservas):
    print("--- NUEVA RESERVA ---")

    auto = _input_int("Ingresar id del auto: ")
    cliente = _input_int("Ingresar id del cliente: ")
    vendedor = _input_int("Ingresar id del vendedor: ")
    monto_reserva = _input_int("Ingresar monto_reserva: ")
    
    
    momento_actual = date.today()
    momento_limite = momento_actual + timedelta(days=30)  # fecha limite


    id = 1 
    if len(lista_reservas) > 0:
        ultima_reserva = lista_reservas[-1]
        id = ultima_reserva["id"] + 1

    nueva_reserva = {
        "id": id, # 1
        "id_auto": auto,  # 12
        "id_cliente": cliente,  # 7
        "id_vendedor": vendedor,  # 2
        "fecha_reserva": momento_actual,  # "2026-06-04"
        "monto_sena": monto_reserva,  # 400000
        "fecha_limite": momento_limite,  # "2026-06-04"
        "estado": ESTADO_RESERVA_ACTIVA,
    }

    lista_reservas.append(nueva_reserva)

    # como lo pide la documentacion
    fecha_limite_texto = momento_limite.strftime("%d-%m-%Y")
    print(f"¡Reserva guardada! Vence el: {fecha_limite_texto}")

#funcion para verificar y actualizar reservas vencidas
def verificar_y_actualizar_vencimientos(lista_reservas):
    fecha_actual = date.today()
    for reserva in lista_reservas:
        if reserva["estado"] == ESTADO_RESERVA_ACTIVA:
            fecha_limite = reserva["fecha_limite"]
            if fecha_actual > fecha_limite:
                reserva["estado"] = ESTADO_RESERVA_CANCELADA

#funcion para mostrar las reservas activas
def listar_reservas_activas(lista_reservas):
    if len(lista_reservas) == 0:
        print("No hay reservas registradas")
        return

    tiene_activas = False
    for nueva_reserva in lista_reservas:
        if nueva_reserva["estado"] == ESTADO_RESERVA_ACTIVA:
            print("-" * 20)
            print(f"ID: {nueva_reserva['id']}")
            print(f"ID del auto: {nueva_reserva['id_auto']}")
            print(f"ID del cliente: {nueva_reserva['id_cliente']}")
            print(f"ID del vendedor: {nueva_reserva['id_vendedor']}")
            print(f"Monto de la reserva: ${nueva_reserva['monto_sena']}")
            print(f"Fecha reserva: {nueva_reserva['fecha_reserva']}")
            print(f"Fecha límite: {nueva_reserva['fecha_limite']}")
            print(f"Estado: {nueva_reserva['estado']}")
            print("-" * 20)
            tiene_activas = True
    
    if not tiene_activas:
        print("No hay reservas activas")


# funcion para buscar reservas
def buscar_reservas(lista_reservas):

    print("1. Buscar por id de auto")
    print("2. Buscar por id de cliente")
    print("3. Buscar por id de vendedor")

    opcion = _input_int("Opcion: ")

    match opcion:
        case 1:
            auto = _input_int("Ingrese id del auto: ")
            encontrado = False 
            for reserva in lista_reservas:
                if reserva["id_auto"] == auto:
                    print("-" * 20)
                    print(f"ID Reserva: {reserva['id']} | Estado: {reserva['estado']} | Monto: ${reserva['monto_sena']}")
                    encontrado = True
            
            if not encontrado:
                print(f"{Color.ROJO}No se encontró ninguna reserva para el auto especificado.{Color.RESET}")

        case 2:
            cliente = _input_int("Ingrese id del cliente: ")
            encontrado = False
            for reserva in lista_reservas:
                if reserva["id_cliente"] == cliente:
                    print("-" * 20)
                    print(f"ID Reserva: {reserva['id']} | Auto: {reserva['id_auto']} | Estado: {reserva['estado']}")
                    encontrado = True
            
            if not encontrado:
                print(f"{Color.ROJO}No se encontró ninguna reserva para el cliente especificado.{Color.RESET}")

        case 3:
            vendedor = _input_int("Ingrese id del vendedor: ")
            encontrado = False
            for reserva in lista_reservas:
                if reserva["id_vendedor"] == vendedor:
                    print("-" * 20)
                    print(f"ID Reserva: {reserva['id']} | Auto: {reserva['id_auto']} | Estado: {reserva['estado']}")
                    encontrado = True
            
            if not encontrado:
                print(f"{Color.ROJO}No se encontró ninguna reserva para el vendedor especificado.{Color.RESET}")

# funcion para concretar ventas
def concretar_venta(lista_reservas):
    print("1. Concretar venta por id de auto")
    print("2. Concretar venta por id de cliente")
    print("3. Concretar venta por id de vendedor")

    opcion = _input_int("Opcion: ")

    match opcion:
        case 1:
            auto = _input_int("Ingrese auto: ")
            for nueva_reserva in lista_reservas:
                if nueva_reserva["id_auto"] == auto:
                    nueva_reserva["monto_sena"] += _input_int("Ingresar monto a saldar: ")
                    nueva_reserva["estado"] = ESTADO_RESERVA_VENTA
                    print("¡Venta concretada y monto actualizado exitosamente!")
                    return
            print("No se encontró una reserva para el auto especificado.")
            return

        case 2:
            cliente = _input_int("Ingrese cliente: ")
            for nueva_reserva in lista_reservas:
                if nueva_reserva["id_cliente"] == cliente:
                    nueva_reserva["monto_sena"] += _input_int("Ingresar monto a saldar: ")
                    nueva_reserva["estado"] = ESTADO_RESERVA_VENTA
                    print("¡Venta concretada y monto actualizado exitosamente!")
                    return
            print("No se encontró una reserva para el cliente especificado.")
            return

        case 3:
            vendedor = _input_int("Ingrese vendedor: ")
            for nueva_reserva in lista_reservas:
                if nueva_reserva["id_vendedor"] == vendedor:
                    nueva_reserva["monto_sena"] += _input_int("Ingresar monto a saldar: ")
                    nueva_reserva["estado"] = ESTADO_RESERVA_VENTA
                    print("¡Venta concretada y monto actualizado exitosamente!")
                    return
            print("No se encontró una reserva para el vendedor especificado.")
            return


# funcion para cancelar reservas
def cancelar_reserva(lista_reservas):
    print("1. Cancelar venta por id de auto")
    print("2. Cancelar venta por id de cliente")
    print("3. Cancelar venta por id de vendedor")

    opcion = _input_int("Opcion: ")

    match opcion:
        case 1:
            auto = _input_int("Ingrese id del auto: ")
            for nueva_reserva in lista_reservas:
                if nueva_reserva["id_auto"] == auto and nueva_reserva["estado"] == ESTADO_RESERVA_ACTIVA:
                    confirmar = input("¿Seguro que quieres cancelar esta reserva? (s/n): ").strip().lower()
                    if confirmar == 's':
                        nueva_reserva["estado"] = ESTADO_RESERVA_CANCELADA
                        print(f"{Color.VERDE}¡Reserva cancelada exitosamente!{Color.RESET}")
                    else:
                        print("Operación abortada. La reserva sigue activa.")
                    return
            print(f"{Color.ROJO}No se encontró una reserva para el auto especificado.{Color.RESET}")
            return
        case 2:
            cliente = _input_int("Ingrese id del cliente: ")
            for nueva_reserva in lista_reservas:
                if nueva_reserva["id_cliente"] == cliente and nueva_reserva["estado"] == ESTADO_RESERVA_ACTIVA:
                    confirmar = input("¿Seguro que quieres cancelar esta reserva? (s/n): ").strip().lower()
                    if confirmar == 's':
                        nueva_reserva["estado"] = ESTADO_RESERVA_CANCELADA
                        print(f"{Color.VERDE}¡Reserva cancelada exitosamente!{Color.RESET}")
                    else:
                        print("Operación abortada. La reserva sigue activa.")
                    return
            print(f"{Color.ROJO}No se encontró una reserva para el cliente especificado.{Color.RESET}")
            return
        case 3:
            vendedor = _input_int("Ingrese id del vendedor: ")
            for nueva_reserva in lista_reservas:
                if nueva_reserva["id_vendedor"] == vendedor and nueva_reserva["estado"] == ESTADO_RESERVA_ACTIVA:
                    confirmar = input("¿Seguro que quieres cancelar esta reserva? (s/n): ").strip().lower()
                    if confirmar == 's':
                        nueva_reserva["estado"] = ESTADO_RESERVA_CANCELADA
                        print(f"{Color.VERDE}¡Reserva cancelada exitosamente!{Color.RESET}")
                    else:
                        print("Operación abortada. La reserva sigue activa.")
                    return
            print(f"{Color.ROJO}No se encontró una reserva para el vendedor especificado.{Color.RESET}")
            return

# Carga el JSON y convierte las fechas de texto a objetos date. Recorremos la lista y transformamos los strings a objetos date
def cargar_reservas_json(ruta_archivo):
  
    try:
        with open(ruta_archivo, 'r') as archivo:
            lista_reservas = json.load(archivo)
            
            
            for reserva in lista_reservas:
                reserva["fecha_reserva"] = date.fromisoformat(reserva["fecha_reserva"])
                reserva["fecha_limite"] = date.fromisoformat(reserva["fecha_limite"])
                
            return lista_reservas

    except FileNotFoundError:
        return []

# Hacemos una copia del diccionario para no romper los dates que están en memoria
def guardar_reservas_json(lista_reservas, ruta_archivo):
 
    reservas_para_guardar = []
    
    for reserva in lista_reservas:
        
        reserva_copia = reserva.copy() # copy es reservada de Python
        
        reserva_copia["fecha_reserva"] = reserva["fecha_reserva"].isoformat()
        reserva_copia["fecha_limite"] = reserva["fecha_limite"].isoformat()
        
        reservas_para_guardar.append(reserva_copia)

    with open(ruta_archivo, 'w') as archivo:
        json.dump(reservas_para_guardar, archivo, indent=4)

def main_reservas():
    ruta = "db/db_reservas.json"
    lista_reservas = []
    lista_reservas = cargar_reservas_json(ruta)
    verificar_y_actualizar_vencimientos(lista_reservas)

    opcion = -1

    while opcion != 9:

        guardar_reservas_json(lista_reservas, ruta)
        print("\n")
        print(f"{Color.CYAN}=== RESERVAS ==={Color.RESET}")

        print(f"{Color.AZUL}1.{Color.RESET} Registrar una nueva reserva ")
        print(f"{Color.AZUL}2.{Color.RESET} Listar reservas activas ")
        print(f"{Color.AZUL}3.{Color.RESET} Buscar reservas ")
        print(f"{Color.AZUL}4.{Color.RESET} Concretar venta ")
        print(f"{Color.AZUL}5.{Color.RESET} Cancelar reserva")
        print(f"{Color.ROJO}9.{Color.RESET} Volver al menú principal")

        print(f"{Color.AMARILLO}Elegi una opcion:{Color.RESET}")
        opcion = _input_int("Seleccione una opcion: ")

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

            case 9:
                print(f"\n{Color.VERDE}*Usted salio del programa*{Color.RESET}")
                break
            case _:  # como el default: en c
                print(f"{Color.ROJO}Opción inválida, vuelve a intentarlo{Color.RESET}")


# main_reservas()

if __name__ == "__main__":
    main_reservas()
