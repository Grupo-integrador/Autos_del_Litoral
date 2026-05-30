from datetime import datetime
from datetime import datetime, timedelta

ESTADO_RESERVA_ACTIVA='activa'
ESTADO_RESERVA_VENTA='venta'
ESTADO_RESERVA_CANCELADA='cancelada'


def registrar_nueva_reserva(lista_reservas):
    print("--- NUEVA RESERVA ---")

    numero_unico = ingresar_entero("Ingresar numero_unico: ")
    auto = input("Ingresar auto: ")
    cliente = input("Ingresar cliente: ")
    vendedor = input("Ingresar vendedor: ")
    monto_reserva = ingresar_float("Ingresar monto_reserva: ")
    
    
    momento_actual = datetime.now()
    momento_limite = momento_actual + timedelta(days=30) #fecha limite
    
    # Convertimos ambas a texto para guardarlas en el diccionario
    fecha_reserva_texto = momento_actual.strftime("%d-%m-%Y")
    fecha_limite_texto = momento_limite.strftime("%d-%m-%Y")
    
    id = 1
    if (len(lista_reservas)>0):
        ultima_reserva = lista_reservas[-1]
        id = ultima_reserva["id_key"]+1

    nueva_reserva = {
        "id_key": id,
        "numero_unico": numero_unico, #345
        "auto": auto, # fiat cronos - AD987CE
        "cliente": cliente, # Carlos López
        "vendedor": vendedor, # Pedro Martínez
        "monto_reserva": monto_reserva, # 400000
        "fecha_reserva": fecha_reserva_texto, # 25-05-2026
        "fecha_limite": fecha_limite_texto, # 25-06-2026
        "estado": ESTADO_RESERVA_ACTIVA
    }
    
    lista_reservas.append(nueva_reserva)
    print(f"¡Reserva guardada! Vence el: {fecha_limite_texto}")

def listar_reservas_activas(lista_reservas):
    for reserva in lista_reservas:
        if reserva["estado"] == ESTADO_RESERVA_ACTIVA:
            print(reserva)
def buscar_reservas():
    pass
def concretar_venta():
    pass
def cancelar_reserva():
    pass

def ingresar_entero(msj:str)->int:
    a_retornar = input(msj)
    while not a_retornar.isnumeric:
        print("El valor ingresado no es numerico!")
        a_retornar = input(msj)
    return int(a_retornar)

def ingresar_float(msj:str)->float:
    a_retornar = input(msj)
    while not a_retornar.isnumeric:
        print("El valor ingresado no es numerico!")
        a_retornar = input(msj)
    return float(a_retornar)

def listar():
    for lista_reserva in lista_reserva:
        print(lista_reserva)

def main_reservas():
        # lista
        lista_reservas = [{}]

        opcion = -1

        while opcion != 0:
            print("\n")
            print("=== RESERVAS ===")
            print("1. Registrar una nueva reserva ")
            print("2. Listar reservas activas ")
            print("3. Buscar reservas ")
            print("4. Concretar venta ")
            print("5. Cancelar reserva")
            print("0. Salir")
            print("Elegi una opcion:")
            opcion = int(input())

            match opcion:
                case 1:
                      registrar_nueva_reserva(lista_reservas) #parametro
                case 2:
                      listar_reservas_activas()
                case 3:
                      buscar_reservas()
                case 4:
                      concretar_venta()  
                case 5:
                      cancelar_reserva()
                    
                case 0:
                    print("\n*Usted salio del programa*")
                    break
                case _:  # como el default: en c
                    print("opcion invalida, vuelve a intentarlo")

main_reservas()