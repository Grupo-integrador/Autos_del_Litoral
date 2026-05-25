def main():

        opcion = -1
        lista = []

        while opcion != 0:
            print("\n")
            print("=== MENU PRINCIPAL ===")
            print("1. Operaciones con listas")
            print("2. Analisis de listas")
            print("3. Trabajar con frases")
            print("0. Salir")
            print("Elegi una opcion:")
            opcion = int(input())

            match opcion:
                case 1:
                    submenu_listas(lista)
                case 2:
                    print("Analisis de listas")
                case 3:
                    print("Trabajar con frases")
                case 0:
                    print("\n*Usted salio del programa*")
                    break
                case _:  # como el default: en c
                    print("opcion invalida, vuelve a intentarlo")
                    
main()