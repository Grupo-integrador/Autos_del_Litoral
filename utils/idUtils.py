from utils.dbUtils import _db_leer_datos


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
