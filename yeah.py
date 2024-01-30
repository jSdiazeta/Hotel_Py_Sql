import tkinter as tk
from tkinter import messagebox
import mysql.connector
import pandas as pd

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
    "numero_de_personas": ["ID_Personas", "ID_Reserva", "Cantidad"],
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

    global tabla_seleccionada
    tabla_seleccionada = tabla

def crear_registro():
    campos = campos_tablas.get(tabla_seleccionada, [])
    values = [entry.get() for entry in entries]

    if all(values):
        campos_str = ", ".join(campos)
        placeholders = ", ".join(["%s"] * len(campos))
        query = f"INSERT INTO {tabla_seleccionada} ({campos_str}) VALUES ({placeholders})"
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Éxito", "Registro creado con éxito.")
        limpiar_campos()
        mostrar_registros()
    else:
        messagebox.showerror("Error", "Todos los campos son requeridos.")

def limpiar_campos():
    for entry in entries:
        entry.delete(0, "end")

def mostrar_registros():
    query = f"SELECT * FROM {tabla_seleccionada}"
    cursor.execute(query)
    registros = cursor.fetchall()
    columnas = campos_tablas.get(tabla_seleccionada, [])
    df = pd.DataFrame(registros, columns=columnas)
    text_registros.delete(1.0, tk.END)  # Limpiar el Text widget
    text_registros.insert(tk.END, df.to_string(index=False))

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

btn_crear = tk.Button(frame_botones, text="Crear Registro", command=crear_registro)
btn_crear.pack(side="left", padx=5)

frame_registros = tk.Frame(root)
frame_registros.pack(padx=20, pady=10)

text_registros = tk.Text(frame_registros, height=10, width=50)
text_registros.pack()

tabla_seleccionada = ""

root.mainloop()
