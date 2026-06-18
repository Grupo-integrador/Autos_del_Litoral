import os


# Funcion para validar entrada de tipo int
def _input_int(mensaje):
    while True:
        try:
            # Si la entrada es válida, la convierte a int y la retorna, rompiendo el bucle
            return int(input(mensaje))
        except ValueError:  # Atrapa la excepción ValueError
            # Avisa del error y vuelve a repetir el bucle
            print(f" ⚠️  {Color.ROJO}Ingrese un número válido.{Color.RESET}")


# Funcion para validar entrada de tipo str
def _input_str(mensaje):
    while True:
        try:
            value = str(input(mensaje))
            if not value:  # Si la entrada está vacía, lanza una excepción
                raise ValueError(
                    "La entrada no puede estar vacía."
                )  # El raise lanza la excepción
            return value
        except ValueError as e:  # Atrapa la excepción ValueError
            print(f" ⚠️  {Color.ROJO}{e}{Color.RESET}")


# Funcion para limpiar la consola
def _limpiar_pantalla():
    # Si el sistema es Windows, usa "cls", de lo contrario usa "clear"
    os.system("cls" if os.name == "nt" else "clear")


# Declaro los colores
class Color:
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
