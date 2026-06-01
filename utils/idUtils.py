from utils.dbUtils import _db_leer_datos


def _id_autoincremental(archivo):
    datos = _db_leer_datos(archivo)

    if (len(datos)) > 0:
        ultimo_dato = datos[-1]
        print("ultimo dato", ultimo_dato)
        id = ultimo_dato["id"] + 1
        print("id", id)
        return id
    else:
        return 1
