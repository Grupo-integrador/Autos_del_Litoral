# Funcion para validar entrada de tipo int
def _input_int(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("  ⚠️  Ingrese un número válido.")
