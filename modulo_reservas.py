import json
from datetime import date, timedelta
from utils.validateUtils import _input_int, Color
from utils.dbUtils import _db_leer_datos
from modulo_ventas import registrar_venta

ESTADO_RESERVA_ACTIVA = "activa"
ESTADO_RESERVA_VENTA = "concretada"
ESTADO_RESERVA_CANCELADA = "cancelada"


# funcion para agregar reservas mediante un diccionario a la lista de reservas
def registrar_nueva_reserva(lista_reservas, lista_autos):
    print("--- NUEVA RESERVA ---")

    auto_id = _input_int("Ingresar id del auto: ")
    auto_encontrado = None
    for a in lista_autos:
        if a["id"] == auto_id:
            auto_encontrado = a
            break

    if not auto_encontrado:
        print(f"{Color.ROJO}No se encontró ningún auto con el ID especificado.{Color.RESET}")
        return

    if auto_encontrado["estado"] != "disponible":
        print(f"{Color.ROJO}El auto no está disponible para reserva (estado actual: {auto_encontrado['estado']}).{Color.RESET}")
        return

    # Validar cliente
    cliente = _input_int("Ingresar id del cliente: ")
    datos_clientes = _db_leer_datos("db/db_clientes.json")
    cliente_encontrado = False
    for c in datos_clientes:
        if c["id"] == cliente:
            cliente_encontrado = True
            break
    if not cliente_encontrado:
        print(f"{Color.ROJO}No se encontró ningún cliente con el ID especificado.{Color.RESET}")
        return

    # Validar vendedor
    vendedor = _input_int("Ingresar id del vendedor: ")
    datos_vendedores = _db_leer_datos("db/db_vendedores.json")
    vendedor_encontrado = False
    for v in datos_vendedores:
        if v["id"] == vendedor:
            vendedor_encontrado = True
            break
    if not vendedor_encontrado:
        print(f"{Color.ROJO}No se encontró ningún vendedor con el ID especificado.{Color.RESET}")
        return

    monto_reserva = _input_int("Ingresar monto_reserva: ")
    
    momento_actual = date.today()
    momento_limite = momento_actual + timedelta(days=30)  # fecha limite

    id = 1 
    if len(lista_reservas) > 0:
        ultima_reserva = lista_reservas[-1]
        id = ultima_reserva["id"] + 1

    nueva_reserva = {
        "id": id, # 1
        "id_auto": auto_id,  # 12
        "id_cliente": cliente,  # 7
        "id_vendedor": vendedor,  # 2
        "fecha_reserva": momento_actual,  # "2026-06-04"
        "monto_sena": monto_reserva,  # 400000
        "fecha_limite": momento_limite,  # "2026-06-04"
        "estado": ESTADO_RESERVA_ACTIVA,
    }

    auto_encontrado["estado"] = "reservado"
    lista_reservas.append(nueva_reserva)

    fecha_limite_texto = momento_limite.strftime("%d-%m-%Y")
    print(f"¡Reserva guardada! Vence el: {fecha_limite_texto}")

#funcion para verificar y actualizar reservas vencidas
def verificar_y_actualizar_vencimientos(lista_reservas, lista_autos):
    fecha_actual = date.today()
    for reserva in lista_reservas:
        if reserva["estado"] == ESTADO_RESERVA_ACTIVA:
            fecha_limite = reserva["fecha_limite"]
            if fecha_actual > fecha_limite:
                reserva["estado"] = ESTADO_RESERVA_CANCELADA
                # Devolvemos el auto a disponible
                for a in lista_autos:
                    if a["id"] == reserva["id_auto"]:
                        a["estado"] = "disponible"
                        break

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

# funcion auxiliar para mostrar el detalle de una reserva
def mostrar_detalle_reserva(reserva):
    print(f"""
    ----------------------------------------
    ID Reserva:      {reserva['id']}
    Estado:          {reserva['estado'].upper()}
    ID del Auto:     {reserva['id_auto']}
    ID del Cliente:  {reserva['id_cliente']}
    ID del Vendedor: {reserva['id_vendedor']}
    Fecha Reserva:   {reserva['fecha_reserva'].strftime('%d-%m-%Y') if hasattr(reserva['fecha_reserva'], 'strftime') else reserva['fecha_reserva']}
    Fecha Límite:    {reserva['fecha_limite'].strftime('%d-%m-%Y') if hasattr(reserva['fecha_limite'], 'strftime') else reserva['fecha_limite']}
    Monto de Seña:   ${reserva['monto_sena']}
    ----------------------------------------
    """)


# funcion auxiliar para filtrar reservas activas por un criterio
def obtener_reservas_activas_por_criterio(lista_reservas, campo, valor):
    coincidencias = []
    for r in lista_reservas:
        if r["estado"] == ESTADO_RESERVA_ACTIVA and r[campo] == valor:
            coincidencias.append(r)
    return coincidencias


# funcion auxiliar para buscar y seleccionar una reserva de forma interactiva y segura
def elegir_reserva_activa(lista_reservas):
    print("1. Buscar por id de auto")
    print("2. Buscar por id de cliente")
    print("3. Buscar por id de vendedor")
    print("4. Buscar por id de reserva")

    opcion = _input_int("Opcion: ")
    campo = None
    mensaje_input = ""

    match opcion:
        case 1:
            campo = "id_auto"
            mensaje_input = "Ingrese id del auto: "
        case 2:
            campo = "id_cliente"
            mensaje_input = "Ingrese id del cliente: "
        case 3:
            campo = "id_vendedor"
            mensaje_input = "Ingrese id del vendedor: "
        case 4:
            campo = "id"
            mensaje_input = "Ingrese id de la reserva: "
        case _:
            print(f"{Color.ROJO}Opción inválida.{Color.RESET}")
            return None

    valor = _input_int(mensaje_input)
    coincidencias = obtener_reservas_activas_por_criterio(lista_reservas, campo, valor)

    if not coincidencias:
        print(f"{Color.ROJO}No se encontró ninguna reserva activa con el criterio especificado.{Color.RESET}")
        return None

    if len(coincidencias) == 1:
        reserva = coincidencias[0]
        print("\nSe encontró la siguiente reserva:")
        mostrar_detalle_reserva(reserva)
        return reserva
    else:
        print(f"\n{Color.AMARILLO}Se encontraron múltiples reservas activas con ese criterio:{Color.RESET}")
        for r in coincidencias:
            mostrar_detalle_reserva(r)
        
        id_elegido = _input_int("Ingrese el ID de la Reserva que desea seleccionar de la lista superior: ")
        for r in coincidencias:
            if r["id"] == id_elegido:
                return r
        print(f"{Color.ROJO}El ID de reserva ingresado no corresponde a ninguna de las opciones listadas.{Color.RESET}")
        return None


# funcion para concretar ventas
def concretar_venta(lista_reservas, lista_autos):
    print("--- CONCRETAR VENTA DE RESERVA ---")
    reserva_a_concretar = elegir_reserva_activa(lista_reservas)
    if not reserva_a_concretar:
        return

    confirmar = input("¿Confirmar la concreción de esta reserva en venta? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Operación abortada. La reserva sigue activa.")
        return

    monto_saldar = _input_int("Ingresar monto a saldar: ")
    reserva_a_concretar["monto_sena"] += monto_saldar
    reserva_a_concretar["estado"] = ESTADO_RESERVA_VENTA

    auto_encontrado = None
    for a in lista_autos:
        if a["id"] == reserva_a_concretar["id_auto"]:
            a["estado"] = "vendido"
            auto_encontrado = a
            break

    # Concretar la venta usando la función registrar_venta de modulo_ventas
    nueva_venta = registrar_venta(
        id_auto=reserva_a_concretar["id_auto"],
        id_cliente=reserva_a_concretar["id_cliente"],
        id_vendedor=reserva_a_concretar["id_vendedor"],
        precio_final=reserva_a_concretar["monto_sena"]
    )

    if nueva_venta:
        print("¡Venta concretada, estado del auto actualizado a 'vendido' y registro de venta creado exitosamente!")


# funcion para cancelar reservas
def cancelar_reserva(lista_reservas, lista_autos):
    print("--- CANCELAR RESERVA ---")
    reserva_a_cancelar = elegir_reserva_activa(lista_reservas)
    if not reserva_a_cancelar:
        return

    confirmar = input("¿Seguro que quieres cancelar esta reserva? (s/n): ").strip().lower()
    if confirmar == 's':
        reserva_a_cancelar["estado"] = ESTADO_RESERVA_CANCELADA

        for a in lista_autos:
            if a["id"] == reserva_a_cancelar["id_auto"]:
                a["estado"] = "disponible"
                break
        print(f"{Color.VERDE}¡Reserva cancelada exitosamente!{Color.RESET}")
    else:
        print("Operación abortada. La reserva sigue activa.")

# Carga el JSON y convierte las fechas de texto a objetos date. Recorremos la lista y transformamos los strings a objetos date
def cargar_reservas_json(ruta_archivo):
  
    try:
        with open(ruta_archivo, 'r') as archivo:
            lista_reservas = json.load(archivo)
            
            for reserva in lista_reservas:
                reserva["fecha_reserva"] = date.fromisoformat(reserva["fecha_reserva"])
                reserva["fecha_limite"] = date.fromisoformat(reserva["fecha_limite"])
                
            return lista_reservas

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_autos_json(lista_autos, ruta_archivo):
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(lista_autos, archivo, indent=4)



# funcion guardar reservas en el archivo json
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
    ruta_reservas = "db/db_reservas.json"
    ruta_autos = "db/db_autos.json"

    lista_reservas = cargar_reservas_json(ruta_reservas)
    lista_autos = _db_leer_datos(ruta_autos)

    verificar_y_actualizar_vencimientos(lista_reservas, lista_autos)
    guardar_reservas_json(lista_reservas, ruta_reservas)
    guardar_autos_json(lista_autos, ruta_autos)

    opcion = -1

    while opcion != 9:
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
                registrar_nueva_reserva(lista_reservas, lista_autos)
                guardar_reservas_json(lista_reservas, ruta_reservas)
                guardar_autos_json(lista_autos, ruta_autos)
            case 2:
                listar_reservas_activas(lista_reservas)
            case 3:
                buscar_reservas(lista_reservas)
            case 4:
                concretar_venta(lista_reservas, lista_autos)
                guardar_reservas_json(lista_reservas, ruta_reservas)
                guardar_autos_json(lista_autos, ruta_autos)
            case 5:
                cancelar_reserva(lista_reservas, lista_autos)
                guardar_reservas_json(lista_reservas, ruta_reservas)
                guardar_autos_json(lista_autos, ruta_autos)

            case 9:
                print(f"\n{Color.VERDE}*Usted salio del programa*{Color.RESET}")
                break
            case _:  # como el default: en c
                print(f"{Color.ROJO}Opción inválida, vuelve a intentarlo{Color.RESET}")



if __name__ == "__main__":
    main_reservas()
