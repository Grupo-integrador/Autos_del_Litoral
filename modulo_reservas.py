# def hola

def main():

        opcion = -1
        lista = []

        while opcion != 0:
            print("\n")
            print("=== RESERVAS ===")
            print("1. Operaciones con listas")
            print("0. Salir")
            print("Elegi una opcion:")
            opcion = int(input())

            match opcion:
                case 1:
                    # submenu_listas(lista)
                #case 2:
                      1
                case 0:
                    print("\n*Usted salio del programa*")
                    break
                case _:  # como el default: en c
                    print("opcion invalida, vuelve a intentarlo")

main()