import tkinter as tk
from tkinter import ttk
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

# Funciones CRUD
def crear_registro():
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    telefono = entry_telefono.get()

    if nombre and correo and telefono:
        query = "INSERT INTO cliente (Nombre, Correo, Telefono) VALUES (%s, %s, %s)"
        values = (nombre, correo, telefono)
        cursor.execute(query, values)
        db.commit()
        messagebox.showinfo("Éxito", "Registro creado con éxito.")
        limpiar_campos()
        mostrar_registros()
    else:
        messagebox.showerror("Error", "Todos los campos son requeridos.")

def mostrar_registros():
    tree.delete(*tree.get_children())
    query = "SELECT * FROM cliente"
    cursor.execute(query)
    registros = cursor.fetchall()
    for registro in registros:
        tree.insert("", "end", values=registro)

def eliminar_registro():
    selected_item = tree.selection()[0]
    id_cliente = tree.item(selected_item, "values")[0]

    if id_cliente:
        query = "DELETE FROM cliente WHERE ID_Cliente = %s"
        value = (id_cliente,)
        cursor.execute(query, value)
        db.commit()
        messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
        limpiar_campos()
        mostrar_registros()

def limpiar_campos():
    entry_id_cliente.delete(0, "end")
    entry_nombre.delete(0, "end")
    entry_correo.delete(0, "end")
    entry_telefono.delete(0, "end")

# Crear la interfaz
root = tk.Tk()
root.title("CRUD para Cliente")

frame_datos = tk.Frame(root)
frame_datos.pack(padx=20, pady=20)

label_id_cliente = tk.Label(frame_datos, text="ID Cliente:")
label_id_cliente.grid(row=0, column=0, padx=10, pady=5)
entry_id_cliente = tk.Entry(frame_datos)
entry_id_cliente.grid(row=0, column=1, padx=10, pady=5)

label_nombre = tk.Label(frame_datos, text="Nombre:")
label_nombre.grid(row=1, column=0, padx=10, pady=5)
entry_nombre = tk.Entry(frame_datos)
entry_nombre.grid(row=1, column=1, padx=10, pady=5)

label_correo = tk.Label(frame_datos, text="Correo:")
label_correo.grid(row=2, column=0, padx=10, pady=5)
entry_correo = tk.Entry(frame_datos)
entry_correo.grid(row=2, column=1, padx=10, pady=5)

label_telefono = tk.Label(frame_datos, text="Teléfono:")
label_telefono.grid(row=3, column=0, padx=10, pady=5)
entry_telefono = tk.Entry(frame_datos)
entry_telefono.grid(row=3, column=1, padx=10, pady=5)

frame_botones = tk.Frame(root)
frame_botones.pack()

btn_crear = tk.Button(frame_botones, text="Crear Registro", command=crear_registro)
btn_crear.pack(side="left", padx=5)

btn_eliminar = tk.Button(frame_botones, text="Eliminar Registro", command=eliminar_registro)
btn_eliminar.pack(side="left", padx=5)

frame_tree = tk.Frame(root)
frame_tree.pack(padx=20, pady=10)

tree = ttk.Treeview(frame_tree, columns=("ID Cliente", "Nombre", "Correo", "Teléfono"), show="headings")
tree.heading("ID Cliente", text="ID Cliente")
tree.heading("Nombre", text="Nombre")
tree.heading("Correo", text="Correo")
tree.heading("Teléfono", text="Teléfono")
tree.pack()

mostrar_registros()

root.mainloop()