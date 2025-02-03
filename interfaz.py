import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import funciones_db as db
from datetime import datetime
import registros as db1
from exportar_excel import generar_excel_obligaciones

def generar_excel_ui():
    """Genera un archivo Excel con las obligaciones de una persona según su número de documento."""
    numero_documento = entry_numero_documento_excel.get().strip()
    
    if not numero_documento:
        messagebox.showerror("Error", "Debe ingresar un número de documento.")
        return

    
    ruta_salida = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Archivos de Excel", "*.xlsx")],
        title="Guardar archivo de obligaciones",
        initialfile=f"Obligaciones_{numero_documento}.xlsx"
    )

    if not ruta_salida:
        messagebox.showwarning("Aviso", "No se seleccionó una ubicación. Operación cancelada.")
        return

    
    try:
        generar_excel_obligaciones(numero_documento, ruta_salida)
        messagebox.showinfo("Éxito", f"Archivo Excel generado correctamente en:\n{ruta_salida}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al generar el Excel:\n{str(e)}")

def registrar_negocio():
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    fecha_inicio = entry_fecha_inicio.get()
    fecha_fin = entry_fecha_fin.get()
    db1.registrar_negocio(nombre, descripcion, fecha_inicio, fecha_fin)
    messagebox.showinfo("Registro", "Negocio Fiduciario registrado exitosamente")
    entry_nombre.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)
    entry_fecha_inicio.delete(0, tk.END)
    entry_fecha_fin.delete(0, tk.END)

def registrar_obligacion():
    descripcion = entry_obligacion_descripcion.get()
    fecha_vencimiento = entry_fecha_vencimiento.get()

    
    try:
        monto = float(entry_monto.get())
    except ValueError:
        messagebox.showerror("Error", "El monto debe ser un número válido")
        return

   
    if not descripcion or not fecha_vencimiento:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    
    try:
        fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Use AAAA-MM-DD")
        return

    
    db1.registrar_obligacion(descripcion, monto, fecha_vencimiento)

    
    messagebox.showinfo("Registro", "Obligación registrada exitosamente")

    
    entry_obligacion_descripcion.delete(0, tk.END)
    entry_monto.delete(0, tk.END)
    entry_fecha_vencimiento.delete(0, tk.END)
    
    
def registrar_persona():
    nombre = entry_persona_nombre.get()
    apellido = entry_persona_apellido.get()
    tipo_documento = combo_tipo_documento.get()
    numero_documento = entry_numero_documento.get()
    db1.registrar_persona(nombre, apellido, tipo_documento, numero_documento)
    messagebox.showinfo("Registro", "Persona registrada exitosamente")
    entry_persona_nombre.delete(0, tk.END)
    entry_persona_apellido.delete(0, tk.END)
    combo_tipo_documento.set("")
    entry_numero_documento.delete(0, tk.END)



def asignar_negocios_ui():
    persona = combo_personas.get()
    if not persona:
        messagebox.showerror("Error", "Debes seleccionar una persona.")
        return

    numero_documento = persona.split(" - ")[0]  
    negocios_seleccionados = [id_negocio for id_negocio, var in checkbox_vars.items() if var.get()]

    if not negocios_seleccionados:
        messagebox.showerror("Error", "Debes seleccionar al menos un negocio.")
        return

    
    negocios_ya_asignados = db.obtener_negocios_asignados(numero_documento)
    negocios_duplicados = [n for n in negocios_seleccionados if n in negocios_ya_asignados]
    negocios_nuevos = [n for n in negocios_seleccionados if n not in negocios_ya_asignados]

    mensaje = ""
    if negocios_duplicados:
        nombres_duplicados = [nombre for id_negocio, nombre in negocios if id_negocio in negocios_duplicados]
        mensaje += f"Los siguientes negocios ya estaban asignados y no se reasignaron: {', '.join(nombres_duplicados)}\n\n"

    if negocios_nuevos:
        if db.asignar_negocios(numero_documento, negocios_nuevos):
            mensaje += "Negocios nuevos asignados correctamente."

    if mensaje:
        messagebox.showinfo("Resultado de la asignación", mensaje)
    else:
        messagebox.showwarning("Aviso", "No se realizaron asignaciones porque todos los negocios seleccionados ya estaban asignados.")
        
        
def asignar_obligaciones_ui():
    """Función para asignar obligaciones a un negocio fiduciario"""
    negocio = combo_negocios.get()
    if not negocio:
        messagebox.showerror("Error", "Debes seleccionar un negocio.")
        return

    id_negocio = negocio.split(" - ")[0]  
    obligaciones_seleccionadas = [id_obligacion for id_obligacion, var in checkbox_vars_obligaciones.items() if var.get()]

    if not obligaciones_seleccionadas:
        messagebox.showerror("Error", "Debes seleccionar al menos una obligación.")
        return

    for id_obligacion in obligaciones_seleccionadas:
        db.asignar_obligacion_a_negocio(id_negocio, id_obligacion)

    messagebox.showinfo("Asignación", "Obligaciones asignadas correctamente.")
    actualizar_asignaciones(None)  


def actualizar_asignaciones(event=None):
    """Actualizar la lista de negocios y obligaciones al cambiar de pestaña"""
    
    combo_negocios["values"] = []
    negocios_actualizados = db.obtener_negocios()
    combo_negocios["values"] = [f"{n[0]} - {n[1]}" for n in negocios_actualizados]

    
    for widget in frame_asignaciones_obligaciones.winfo_children():
        if isinstance(widget, ttk.Checkbutton):
            widget.destroy()

    
    global checkbox_vars_obligaciones  
    checkbox_vars_obligaciones = {}
    obligaciones_actualizadas = db.obtener_obligaciones()
    row_num = 1
    for id_obligacion, descripcion in obligaciones_actualizadas:
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(frame_asignaciones_obligaciones, text=descripcion, variable=var)
        checkbox.grid(row=row_num, column=0, sticky="w", padx=10, pady=5)
        checkbox_vars_obligaciones[id_obligacion] = var
        row_num += 1

    
def crear_checkbuttons(frame, datos, diccionario_vars):
    """Función para crear checkbuttons dinámicamente."""
    diccionario_vars.clear()
    for idx, (id_item, descripcion) in enumerate(datos):
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(frame, text=descripcion, variable=var)
        checkbox.grid(row=idx + 1, column=0, sticky="w", padx=10, pady=5)
        diccionario_vars[id_item] = var
        
        

root = tk.Tk()
root.title("Gestión de Negocios Fiduciarios")
root.geometry("800x600")
root.configure(bg="#f4f4f4")


style = ttk.Style()
style.configure("TNotebook", background="#f4f4f4", padding=10)
style.configure("TNotebook.Tab", padding=[10, 5], font=("Arial", 10, "bold"))
style.configure("TButton", font=("Arial", 10, "bold"), background="#0078D7", foreground="black")
style.configure("TLabel", font=("Arial", 10), background="#f4f4f4")
style.configure("TEntry", font=("Arial", 10))
style.configure("TCombobox", font=("Arial", 10))


notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill="both")
notebook.bind("<<NotebookTabChanged>>", actualizar_asignaciones)




frame_asignaciones = ttk.Frame(notebook)
notebook.add(frame_asignaciones, text="Asignar negocios a una persona")


frame_asignaciones_obligaciones = ttk.Frame(notebook)
notebook.add(frame_asignaciones_obligaciones, text="Asignar Obligaciones a Negocios")


frame_registrar_negocio = ttk.Frame(notebook)
notebook.add(frame_registrar_negocio, text="Registrar Negocio Fiduciario")


frame_registrar_obligacion = ttk.Frame(notebook)
notebook.add(frame_registrar_obligacion, text="Registrar Obligación")


frame_registrar_persona = ttk.Frame(notebook)
notebook.add(frame_registrar_persona, text="Registrar Persona")


frame_generar_excel = ttk.Frame(notebook)
notebook.add(frame_generar_excel, text="Generar Excel")


obligaciones = db.obtener_obligaciones()
checkbox_vars_obligaciones = {}
row_num = 1
for id_obligacion, descripcion in obligaciones:
    var = tk.BooleanVar()
    checkbox = ttk.Checkbutton(frame_asignaciones_obligaciones, text=descripcion, variable=var)
    checkbox.grid(row=row_num, column=0, sticky="w", padx=10, pady=5)
    checkbox_vars_obligaciones[id_obligacion] = var
    row_num += 1


negocios = db.obtener_negocios()
checkbox_vars = {}
row_num = 1
for id_negocio, nombre in negocios:
    var = tk.BooleanVar()
    checkbox = ttk.Checkbutton(frame_asignaciones, text=nombre, variable=var)
    checkbox.grid(row=row_num, column=0, sticky="w", padx=10, pady=5)
    checkbox_vars[id_negocio] = var
    row_num += 1


btn_asignar_obligaciones = ttk.Button(frame_asignaciones_obligaciones, text="Asignar Obligaciones", command=asignar_obligaciones_ui)
btn_asignar_obligaciones.grid(row=row_num, column=0, columnspan=2, pady=10)


personas = db.obtener_personas()
combo_personas = ttk.Combobox(frame_asignaciones, values=[f"{p[0]} - {p[1]}" for p in personas])
combo_personas.grid(row=0, column=1, padx=10, pady=10)


btn_asignar = ttk.Button(frame_asignaciones, text="Asignar Negocios", command=asignar_negocios_ui)
btn_asignar.grid(row=row_num, column=0, columnspan=2, pady=10)


ttk.Label(frame_asignaciones_obligaciones, text="Seleccione un negocio:").grid(row=0, column=0, padx=10, pady=10)
combo_negocios = ttk.Combobox(frame_asignaciones_obligaciones)
combo_negocios.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(frame_asignaciones, text="Seleccione una persona:").grid(row=0, column=0, padx=10, pady=10)
combo_personas = ttk.Combobox(frame_asignaciones, values=[f"{p[0]} - {p[1]}" for p in personas])
combo_personas.grid(row=0, column=1, padx=10, pady=10)




ttk.Label(frame_generar_excel, text="Número de Documento:").grid(row=0, column=0, padx=10, pady=10)
entry_numero_documento_excel = ttk.Entry(frame_generar_excel)
entry_numero_documento_excel.grid(row=0, column=1, padx=10, pady=10)


btn_generar_excel = ttk.Button(frame_generar_excel, text="Generar Excel", command=generar_excel_ui)
btn_generar_excel.grid(row=1, column=0, columnspan=2, pady=10)


ttk.Label(frame_registrar_negocio, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
entry_nombre = ttk.Entry(frame_registrar_negocio)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(frame_registrar_negocio, text="Descripción:").grid(row=1, column=0, padx=10, pady=10)
entry_descripcion = ttk.Entry(frame_registrar_negocio)
entry_descripcion.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(frame_registrar_negocio, text="Fecha de inicio (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
entry_fecha_inicio = ttk.Entry(frame_registrar_negocio)
entry_fecha_inicio.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(frame_registrar_negocio, text="Fecha de fin (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=10)
entry_fecha_fin = ttk.Entry(frame_registrar_negocio)
entry_fecha_fin.grid(row=3, column=1, padx=10, pady=10)

ttk.Button(frame_registrar_negocio, text="Registrar", command=registrar_negocio).grid(row=4, column=0, columnspan=2, pady=10)



ttk.Label(frame_registrar_obligacion, text="Descripción:").grid(row=0, column=0, padx=10, pady=10)
entry_obligacion_descripcion = ttk.Entry(frame_registrar_obligacion)
entry_obligacion_descripcion.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(frame_registrar_obligacion, text="Monto:").grid(row=1, column=0, padx=10, pady=10)
entry_monto = ttk.Entry(frame_registrar_obligacion)
entry_monto.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(frame_registrar_obligacion, text="Fecha de vencimiento (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
entry_fecha_vencimiento = ttk.Entry(frame_registrar_obligacion)
entry_fecha_vencimiento.grid(row=2, column=1, padx=10, pady=10)

ttk.Button(frame_registrar_obligacion, text="Registrar", command=registrar_obligacion).grid(row=3, column=0, columnspan=2, pady=10)



ttk.Label(frame_registrar_persona, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
entry_persona_nombre = ttk.Entry(frame_registrar_persona)
entry_persona_nombre.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(frame_registrar_persona, text="Apellido:").grid(row=1, column=0, padx=10, pady=10)
entry_persona_apellido = ttk.Entry(frame_registrar_persona)
entry_persona_apellido.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(frame_registrar_persona, text="Tipo de documento:").grid(row=2, column=0, padx=10, pady=10)
combo_tipo_documento = ttk.Combobox(frame_registrar_persona, values=["Tarjeta de Identidad", "Cédula de Ciudadanía", "Pasaporte"])
combo_tipo_documento.grid(row=2, column=1, padx=10, pady=10)


ttk.Label(frame_registrar_persona, text="Número de documento:").grid(row=3, column=0, padx=10, pady=10)
entry_numero_documento = ttk.Entry(frame_registrar_persona)
entry_numero_documento.grid(row=3, column=1, padx=10, pady=10)

ttk.Button(frame_registrar_persona, text="Registrar", command=registrar_persona).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
