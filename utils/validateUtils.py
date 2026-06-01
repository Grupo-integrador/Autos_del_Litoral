# Funcion para validar entrada de tipo int
def _input_int(mensaje):
    while True:
        try:
            # Si la entrada es válida, la convierte a int y la retorna, rompiendo el bucle
            return int(input(mensaje))
        except ValueError:  # Atrapa la excepción ValueError
            # Avisa del error y vuelve a repetir el bucle
            print(" ⚠️  Ingrese un número válido.")


# Declaro los colores
class Color:
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

