import tkinter as tk
from tkinter import ttk, messagebox
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
def crear_registro(tabla):
    if tabla == "Reserva":
        id_reserva = entry_id_reserva.get()
        fecha_reserva = entry_fecha_reserva.get()
        id_cliente = entry_id_cliente.get()
        total_pago = entry_total_pago.get()

        if id_reserva and fecha_reserva and id_cliente and total_pago:
            query = "INSERT INTO Reserva (ID_Reserva, Fecha_Reserva, ID_Cliente, Total_Pago) VALUES (%s, %s, %s, %s)"
            values = (id_reserva, fecha_reserva, id_cliente, total_pago)
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Éxito", "Registro creado con éxito.")
            limpiar_campos()
            mostrar_registros("Reserva")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos.")

    elif tabla == "numero_de_personas":
        id_personas = entry_id_personas.get()
        id_reserva = entry_id_reserva_personas.get()
        cantidad = entry_cantidad.get()

        if id_personas and id_reserva and cantidad:
            query = "INSERT INTO numero_de_personas (ID_Personas, ID_Reserva, Cantidad) VALUES (%s, %s, %s)"
            values = (id_personas, id_reserva, cantidad)
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Éxito", "Registro creado con éxito.")
            limpiar_campos()
            mostrar_registros("numero_de_personas")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos.")

def mostrar_registros(tabla):
    tree.delete(*tree.get_children())
    query = f"SELECT * FROM {tabla}"
    cursor.execute(query)
    registros = cursor.fetchall()
    for registro in registros:
        tree.insert("", "end", values=registro)

def eliminar_registro(tabla):
    selected_item = tree.selection()[0]
    id_reserva = tree.item(selected_item, "values")[0]

    if id_reserva:
        query = f"DELETE FROM {tabla} WHERE ID_Reserva = %s"
        value = (id_reserva,)
        cursor.execute(query, value)
        db.commit()
        messagebox.showinfo("Éxito", "Registro eliminado con éxito.")
        limpiar_campos()
        mostrar_registros(tabla)

def limpiar_campos():
    entry_id_reserva.delete(0, "end")
    entry_fecha_reserva.delete(0, "end")
    entry_id_cliente.delete(0, "end")
    entry_total_pago.delete(0, "end")
    entry_id_personas.delete(0, "end")
    entry_id_reserva_personas.delete(0, "end")
    entry_cantidad.delete(0, "end")

def cargar_campos(tabla):
    if tabla == "Reserva":
        limpiar_campos()
        entry_id_reserva.insert(0, "ID_Reserva")
        entry_fecha_reserva.insert(0, "Fecha_Reserva")
        entry_id_cliente.insert(0, "ID_Cliente")
        entry_total_pago.insert(0, "Total_Pago")

    elif tabla == "numero_de_personas":
        limpiar_campos()
        entry_id_personas.insert(0, "ID_Personas")
        entry_id_reserva_personas.insert(0, "ID_Reserva")
        entry_cantidad.insert(0, "Cantidad")

# Crear la interfaz
root = tk.Tk()
root.title("CRUD con MySQL")

frame_botones_tablas = tk.Frame(root)
frame_botones_tablas.pack(padx=20, pady=20)

btn_reserva = tk.Button(frame_botones_tablas, text="Reserva", command=lambda: cargar_campos("Reserva"))
btn_reserva.pack(side="left", padx=5)

btn_personas = tk.Button(frame_botones_tablas, text="Número de Personas", command=lambda: cargar_campos("numero_de_personas"))
btn_personas.pack(side="left", padx=5)

frame_datos = tk.Frame(root)
frame_datos.pack(padx=20, pady=20)

tk.Label(frame_datos, text="ID Reserva:").grid(row=0, column=0, sticky="e")
entry_id_reserva = tk.Entry(frame_datos)
entry_id_reserva.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_datos, text="Fecha Reserva:").grid(row=1, column=0, sticky="e")
entry_fecha_reserva = tk.Entry(frame_datos)
entry_fecha_reserva.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_datos, text="ID Cliente:").grid(row=2, column=0, sticky="e")
entry_id_cliente = tk.Entry(frame_datos)
entry_id_cliente.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_datos, text="Total Pago:").grid(row=3, column=0, sticky="e")
entry_total_pago = tk.Entry(frame_datos)
entry_total_pago.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame_datos, text="ID Personas:").grid(row=4, column=0, sticky="e")
entry_id_personas = tk.Entry(frame_datos)
entry_id_personas.grid(row=4, column=1, padx=10, pady=5)

tk.Label(frame_datos, text="ID Reserva (Personas):").grid(row=5, column=0, sticky="e")
entry_id_reserva_personas = tk.Entry(frame_datos)
entry_id_reserva_personas.grid(row=5, column=1, padx=10, pady=5)

tk.Label(frame_datos, text="Cantidad:").grid(row=6, column=0, sticky="e")
entry_cantidad = tk.Entry(frame_datos)
entry_cantidad.grid(row=6, column=1, padx=10, pady=5)

frame_botones = tk.Frame(root)
frame_botones.pack()

btn_crear = tk.Button(frame_botones, text="Crear Registro", command=lambda: crear_registro(tabla_seleccionada.get()))
btn_crear.pack(side="left", padx=5)

btn_eliminar = tk.Button(frame_botones, text="Eliminar Registro", command=lambda: eliminar_registro(tabla_seleccionada.get()))
btn_eliminar.pack(side="left", padx=5)

frame_tree = tk.Frame(root)
frame_tree.pack(padx=20, pady=10)

tree = ttk.Treeview(frame_tree, columns=("ID Reserva", "Fecha Reserva", "ID Cliente", "Total Pago"), show="headings")
tree.heading("ID Reserva", text="ID Reserva")
tree.heading("Fecha Reserva", text="Fecha Reserva")
tree.heading("ID Cliente", text="ID Cliente")
tree.heading("Total Pago", text="Total Pago")
tree.pack()

tabla_seleccionada = tk.StringVar()
tabla_seleccionada.set("Reserva")

root.mainloop()
