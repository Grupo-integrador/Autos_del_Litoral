def registrar_nueva_reserva():
    pass
def listar_reservas_activas():
    pass
def buscar_reservas():
    pass
def concretar_venta():
    pass
def cancelar_reserva():
    pass
def main_reservas():

        opcion = -1
        lista = []

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
                      registrar_nueva_reserva
                case 2:
                      listar_reservas_activas
                case 3:
                      buscar_reservas   
                case 4:
                      concretar_venta    
                case 5:
                      cancelar_reserva
                    
                case 0:
                    print("\n*Usted salio del programa*")
                    break
                case _:  # como el default: en c
                    print("opcion invalida, vuelve a intentarlo")

main_reservas()