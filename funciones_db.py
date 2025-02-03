from sqlalchemy import text
import conexion



def asignar_obligacion_a_negocio(id_negocio, id_obligacion):
    query = text("""
        INSERT INTO Negocio_Obligacion (Id_Negocio_Fiduciario, id_obligacion) 
        VALUES (:id_negocio, :id_obligacion)
    """)
    params = {
        'id_negocio': id_negocio,
        'id_obligacion': id_obligacion
    }
    
    try:
        with conexion.obtener_conexion() as conn:
            with conn.begin():
                conn.execute(query, params)
        print("Obligación asignada al negocio con éxito.")
    except Exception as e:
        print(f"Error al asignar la obligación al negocio: {e}")



def asignar_negocios(numero_documento, negocios_seleccionados):
    negocios_asignados = obtener_negocios_asignados(numero_documento)  

    query_insert = text("""
        INSERT INTO Participantes_Negocio (Numero_de_documento, Id_Negocio_Fiduciario) 
        VALUES (:numero_documento, :id_negocio)
    """)

    nuevos_asignados = [id_negocio for id_negocio in negocios_seleccionados if id_negocio not in negocios_asignados]

    if not nuevos_asignados:
        return False  
    
    with conexion.obtener_conexion() as conn:
        with conn.begin():
            for id_negocio in nuevos_asignados:
                conn.execute(query_insert, {"numero_documento": numero_documento, "id_negocio": id_negocio})

    return True  


def obtener_obligaciones():
    query = text("SELECT Id_Obligacion, Descripcion FROM Obligacion")

    with conexion.obtener_conexion() as conn:
        result = conn.execute(query).fetchall()

    return [(row[0], row[1]) for row in result]



def obtener_personas():
    query = text("SELECT Numero_de_documento, Nombre FROM Personas_Participantes")
    
    with conexion.obtener_conexion() as conn:
        result = conn.execute(query).fetchall()
    
    return [(row[0], row[1]) for row in result]  


def obtener_negocios():
    query = text("SELECT Id_Negocio_Fiduciario, Nombre FROM Negocio_Fiduciario")
    
    with conexion.obtener_conexion() as conn:
        result = conn.execute(query).fetchall()
    
    return [(row[0], row[1]) for row in result]  

def obtener_negocios_asignados(numero_documento):
    query = text("""
        SELECT Id_Negocio_Fiduciario 
        FROM Participantes_Negocio 
        WHERE Numero_de_documento = :numero_documento
    """)
    
    with conexion.obtener_conexion() as conn:
        result = conn.execute(query, {"numero_documento": numero_documento}).fetchall()
    
    return {row[0] for row in result}  


