import pandas as pd

import os
import sys
sys.path.append("C:/Users/juane/OneDrive/Escritorio/Prueba tecnica/.venv/Lib/site-packages")

import msoffcrypto
import tkinter as tk
from tkinter import filedialog
from sqlalchemy import text
import conexion as db

def generar_excel_obligaciones(numero_documento, ruta_salida=None):
    """
    Genera un archivo Excel con las obligaciones de los negocios fiduciarios asociados a una persona,
    protegiéndolo con la identificación como contraseña de apertura.
    """

    print(f" Iniciando generación de Excel para el documento: {numero_documento}...")

    query = text("""
        SELECT 
            pp.Numero_de_documento AS Documento,
            pp.Nombre AS Nombre_Persona,
            pp.Apellido AS Apellido_Persona,
            nf.Id_Negocio_Fiduciario AS ID_Negocio,
            nf.Nombre AS Nombre_Negocio,
            nf.Fecha_de_inicio,  
            nf.Fecha_de_fin,     
            ob.Id_Obligacion AS ID_Obligacion,
            ob.Descripcion AS Descripcion_Obligacion,
            ob.Monto AS Monto_Obligacion,
            ob.Fecha_de_vencimiento
        FROM 
            dbo.Personas_Participantes AS pp  
        JOIN 
            dbo.Participantes_Negocio AS pn 
            ON pp.Numero_de_documento = pn.Numero_de_documento
        JOIN 
            dbo.Negocio_Fiduciario AS nf 
            ON pn.Id_Negocio_Fiduciario = nf.Id_Negocio_Fiduciario
        JOIN 
            dbo.Negocio_Obligacion AS no 
            ON nf.Id_Negocio_Fiduciario = no.Id_Negocio_Fiduciario
        JOIN 
            dbo.Obligacion AS ob 
            ON no.Id_Obligacion = ob.Id_Obligacion
        WHERE 
            pp.Numero_de_documento = :numero_documento;
    """)

   
    with db.obtener_conexion() as conn:
        result = conn.execute(query, {"numero_documento": numero_documento}).fetchall()

    if not result:
        print(" No se encontraron obligaciones para esta persona.")
        return

    
    df = pd.DataFrame(result, columns=[
        "Documento", "Nombre_Persona", "Apellido_Persona", "ID_Negocio", "Nombre_Negocio", 
        "Fecha_de_inicio", "Fecha_de_fin", "ID_Obligacion", "Descripcion_Obligacion", 
        "Monto_Obligacion", "Fecha_de_vencimiento"
    ])

    
    for col in ["Fecha_de_inicio", "Fecha_de_fin", "Fecha_de_vencimiento"]:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')

    
    if ruta_salida is None:
        root = tk.Tk()
        root.withdraw()  
        ruta_salida = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")],
            title="Guardar archivo de obligaciones",
            initialfile=f"Obligaciones_{numero_documento}.xlsx"
        )
        if not ruta_salida:  
            print(" No se seleccionó una ubicación. Operación cancelada.")
            return

    temp_filename = f"temp_obligaciones_{numero_documento}.xlsx"

    
    print(f" Guardando archivo temporal: {temp_filename}...")
    writer = pd.ExcelWriter(temp_filename, engine='openpyxl')
    df.to_excel(writer, sheet_name="Obligaciones", index=False)

    
    workbook = writer.book
    worksheet = writer.sheets["Obligaciones"]

    
    for col in worksheet.columns:
        max_length = max([len(str(cell.value)) if cell.value else 0 for cell in col])
        col_letter = col[0].column_letter
        worksheet.column_dimensions[col_letter].width = max_length + 5  

    
    for row in worksheet.iter_rows():
        for cell in row:
            worksheet.row_dimensions[cell.row].height = 25  

    writer.close()  

    
    print("Protegiendo el archivo con contraseña...")
    with open(temp_filename, "rb") as f_in, open(ruta_salida, "wb") as f_out:
        encrypted = msoffcrypto.OfficeFile(f_in)
        encrypted.encrypt(str(numero_documento), f_out)  # Usa el número de documento como contraseña

    
    os.remove(temp_filename)

    print(f" Archivo generado con éxito: {ruta_salida}")

