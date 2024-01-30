import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="hotel"
)
cursor = db.cursor()

# Campos para cada tabla
campos_tablas = {
    "Reserva": ["ID_Reserva", "Fecha_Reserva", "ID_Cliente", "Total_Pago"],
    "numero_de_personas": ["ID_Cliente", "ID_Reserva", "Cantidad"],
    # Agrega las demás tablas aquí con sus campos
}

# Funciones
def cargar_campos(tabla):
    for entry in entries:
        entry.grid_forget()

    campos = campos_tablas.get(tabla, [])
    for i, campo in enumerate(campos):
        entry = tk.Entry(frame_datos)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, campo)
        entries.append(entry)

def crear_registro(tabla):
    campos = campos_tablas.get(tabla, [])
    values = [entry.get() for entry in entries]

    if all(values):
        campos_str = ", ".join(campos)
        placeholders = ", ".join(["%s"] * len(campos))
        query = f"INSERT INTO {tabla} ({campos_str}) VALUES ({placeholders})"
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Éxito", "Registro creado con éxito.")
        limpiar_campos()
    else:
        messagebox.showerror("Error", "Todos los campos son requeridos.")

def limpiar_campos():
    for entry in entries:
        entry.delete(0, "end")

# Crear la interfaz
root = tk.Tk()
root.title("Inserción de Registros")

frame_botones_tablas = tk.Frame(root)
frame_botones_tablas.pack(padx=20, pady=20)

btn_reserva = tk.Button(frame_botones_tablas, text="Reserva", command=lambda: cargar_campos("Reserva"))
btn_reserva.pack(side="left", padx=5)

btn_personas = tk.Button(frame_botones_tablas, text="Número de Personas", command=lambda: cargar_campos("numero_de_personas"))
btn_personas.pack(side="left", padx=5)

# Agrega más botones para las demás tablas aquí

frame_datos = tk.Frame(root)
frame_datos.pack(padx=20, pady=20)

entries = []

frame_botones = tk.Frame(root)
frame_botones.pack()

btn_crear = tk.Button(frame_botones, text="Crear Registro", command=lambda: crear_registro(tabla_seleccionada.get()))
btn_crear.pack(side="left", padx=5)

root.mainloop()
