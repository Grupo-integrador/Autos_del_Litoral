import json


# Funcion para inyectar datos en un archivo JSON, EJ: _db_inyectar_datos("db_ventas.json", data)
def _db_inyectar_datos(archivo, data):

    # Leemos el archivo y verificamos si contiene datos
    with open(archivo, "r", encoding="utf-8") as lectura_archivo:
        try:
            contenido = json.load(lectura_archivo)
        # Si el archivo no contiene datos, inicializamos la lista vacia
        except json.JSONDecodeError:
            contenido = []

    # Agregamos los datos a la lista
    contenido.append(data)

    # Parseamos la data a JSON
    dump_json = json.dumps(
        contenido,
        indent=4,
    )

    # Creamos un archivo si no existe y escribimos la data
    with open(archivo, "w", encoding="utf-8") as db_ventas:
        db_ventas.write(dump_json)
    # Retornamos el JSON parseado que contiene los datos inyectados en DB
    return dump_json


# Funcion para leer los datos de un archivo JSON, EJ: _db_leer_datos("db_ventas.json")
def _db_leer_datos(archivo):
    # Leemos el archivo y retornamos el contenido parseado
    with open(archivo, "r", encoding="utf-8") as lectura_archivo:
        try:
            contenido = json.load(lectura_archivo)
        # Si el archivo no contiene datos, inicializamos la lista vacia
        except json.JSONDecodeError:
            contenido = []

        # Retornamos el contenido parseado
        return contenido
