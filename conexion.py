from sqlalchemy import create_engine

def obtener_conexion():
    server = 'localhost'
    database = 'NegociosFiduciarios2'  
    connection_string = f'mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    return engine.connect()

