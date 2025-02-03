from exportar_excel import generar_excel_obligaciones

def test_generar_excel():
    
    numero_documento = "1007480748"
    
    print(" Iniciando prueba de generación de Excel...")

    
    generar_excel_obligaciones(numero_documento)

    print(" Prueba finalizada: Archivo Excel generado.")

if __name__ == "__main__":
    test_generar_excel()
