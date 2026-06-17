from utils.dbUtils import _db_leer_datos
from utils.validateUtils import _input_int


def _id_autoincremental(archivo):
    datos = _db_leer_datos(archivo)

    if (len(datos)) > 0:
        ultimo_dato = datos[-1]
        id = ultimo_dato["id"] + 1
        return id
    else:
        return 1


# Autoincremental para generar IDs unicos, recibe el nombre del archivo
# Trae los datos del archivo
# if (len(datos)) > 0 Verifica si hay datos
# Si hay datos, devuelve el siguiente ID disponible, si no, devuelve 1


# Buscar una venta por un campo específico (id_auto, id_cliente, id_vendedor)
def _buscar_venta_por_id_modulo(id, archivo, id_modulo):
    datos = _db_leer_datos(archivo)

    # Recorremos la lista de datos y buscamos el ID especificado y retornamos el dato encontrado
    for data_id in datos:
        if data_id[id_modulo] == id:
            return data_id

    return None  # Retornamos None si no se encuentra ninguna venta con ese ID


# Buscar ventas por un campo específico (id_auto, id_cliente, id_vendedor)
def _buscar_ventas_por_id_modulo(id, archivo, id_modulo):
    datos = _db_leer_datos(archivo)

    # Inicializamos una lista para almacenar los resultados
    resultados = []
    # Recorremos la lista de datos y buscamos los IDs especificados y los agregamos a la lista de resultados
    for data_id in datos:
        if data_id[id_modulo] == id:
            resultados.append(data_id)
    return resultados if resultados else None


# Función para buscar un valor por su ID en un archivo
def _buscar_por_id(archivo, id):
    datos = _db_leer_datos(archivo)

    for d in datos:
        if d["id"] == id:
            return d
    return None


# Función para buscar un registro por ID y validar su existencia
def _buscar_por_id_validado(archivo, mensaje):
    while True:
        id_ingresado = _input_int(mensaje)
        resultado = _buscar_por_id(archivo, id_ingresado)
        if resultado is not None:
            return resultado
        print(f"El ID {id_ingresado} no se encontró. Intentá de nuevo.")
