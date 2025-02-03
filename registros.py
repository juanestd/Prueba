from sqlalchemy import text
import conexion

def registrar_negocio(nombre, descripcion, fecha_inicio, fecha_fin):
    query = text("""
        INSERT INTO Negocio_Fiduciario (Nombre, Descripción, Fecha_de_inicio, Fecha_de_fin) 
        VALUES (:nombre, :descripcion, :fecha_inicio, :fecha_fin)
    """)
    params = {
        'nombre': nombre,
        'descripcion': descripcion,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    }
    
    try:
        with conexion.obtener_conexion() as conn:
            with conn.begin():
                conn.execute(query, params)
        print("Negocio fiduciario registrado con éxito.")
    except Exception as e:
        print(f"Error al registrar el negocio fiduciario: {e}")




def registrar_obligacion(Descripcion, monto, fecha_vencimiento):
    query = text("""
        INSERT INTO Obligacion (Descripcion, Monto, Fecha_de_vencimiento)
        VALUES (:Descripcion, :monto, :fecha_vencimiento)
    """)

    params = {
        'Descripcion': Descripcion,  
        'monto': monto,
        'fecha_vencimiento': fecha_vencimiento
    }

    try:
        with conexion.obtener_conexion() as conn:
            with conn.begin():
                conn.execute(query, params)
        print("Obligación registrada con éxito.")
    except Exception as e:
        print(f"Error al registrar la obligación: {e}")

def registrar_persona(nombre, apellido, tipo_documento, numero_documento):
    query = text("""
        INSERT INTO Personas_Participantes (Nombre, Apellido, Tipo_de_documento, Numero_de_documento)
        VALUES (:nombre, :apellido, :tipo_documento, :numero_documento)
    """)

    params = {
        'nombre': nombre,
        'apellido': apellido,
        'tipo_documento': tipo_documento,
        'numero_documento': numero_documento
    }

    try:
        with conexion.obtener_conexion() as conn:
            with conn.begin():
                conn.execute(query, params)
        print("Persona registrada con éxito.")
    except Exception as e:
        print(f"Error al registrar la persona: {e}")
        
        