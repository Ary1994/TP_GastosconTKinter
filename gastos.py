import sqlite3
from tkinter import END
from tkinter import ttk
from tkinter import *

class GastosManager:
    vista_lista_gastos_frame = None 
    def __init__(self,main_window):
        self.conexion = sqlite3.connect("mi_basededatos.db")
        self.main_window = main_window
        
    def agregar_gasto(self, nombre, cantidad, fecha, categoria):
        try:
            # Conectarse a la base de datos (o crearla si no existe)
            conexion = sqlite3.connect("mi_basededatos.db")
            cursor = conexion.cursor()

            # Crear una tabla si no existe
            cursor.execute("CREATE TABLE IF NOT EXISTS gastos (id INTEGER PRIMARY KEY, nombre TEXT, cantidad REAL, fecha TEXT, categoria TEXT)")

            # Insertar los datos del formulario en la tabla
            cursor.execute("INSERT INTO gastos (nombre, cantidad, fecha, categoria) VALUES (?, ?, ?, ?)",
                        (nombre, cantidad, fecha, categoria))

            # Confirmar la transacción
            conexion.commit()

            print("Gasto agregado exitosamente en la base de datos.")
            self.vista_lista_gastos()
        except sqlite3.Error as error:
            print("Error al agregar el gasto en la base de datos:", error)
        finally:
            # Cerrar la conexión a la base de datos
            if conexion:
                conexion.close()

        

   
    def obtener_lista_gastos(self, lista_gastos):
        try:
            conexion = sqlite3.connect("mi_basededatos.db")
            cursor = conexion.cursor()

            # Consulta SQL para obtener los gastos
            cursor.execute("SELECT nombre, cantidad, fecha, categoria FROM gastos")
            gastos = cursor.fetchall()

            # Limpiar el Listbox antes de agregar nuevos datos
            lista_gastos.delete(0, END)
        
            # Agregar los gastos al Listbox
            for gasto in gastos:
                lista_gastos.insert(END, f"{gasto[0]} x {gasto[1]},\n Fecha: {gasto[2]}, Cat: {gasto[3]}")
            conexion.commit()

        except sqlite3.Error as error:
            print("Error al obtener la lista de gastos:", error)
        finally:
            if conexion:
                conexion.close()


    def editar_gasto(self, gasto_id):
        # Implementar la función para editar un gasto
        pass

    def guardar_cambios(self, gasto_id, nombre, cantidad, fecha, categoria):
        # Implementar la función para guardar cambios en un gasto
        pass

    def eliminar_gasto(self, gasto_id):
        # Implementar la función para eliminar un gasto
        pass
    def obtener_valores_y_agregar_gasto(self, nombre_entry, cantidad_entry, fecha_entry, categoria_combobox):
        nombre = nombre_entry.get()
        cantidad = float(cantidad_entry.get())
        fecha = fecha_entry.get()
        categoria = categoria_combobox.get()
        self.agregar_gasto(nombre, cantidad, fecha, categoria)

    def vista_lista_gastos(self, tree, page3):
        # Limpiar la tabla antes de insertar nuevos registros
        for item in tree.get_children():
            tree.delete(item)

        conn = sqlite3.connect("mi_basededatos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, cantidad, fecha, categoria FROM gastos ORDER BY id DESC")
        rows = cursor.fetchall()

        for row in rows:
            id_gasto, nombre_gasto, cantidad_gasto, fecha_gasto, categoria_gasto = row
            editar_button = Button(page3, text="Editar", command=lambda id_gasto=id_gasto: self.editar_gasto(id_gasto))
            eliminar_button = Button(page3, text="Eliminar", command=lambda id_gasto=id_gasto: self.eliminar_gasto(id_gasto))
         
            tree.insert("", "end", values=(nombre_gasto, cantidad_gasto, fecha_gasto, categoria_gasto, editar_button, eliminar_button))

        conn.close()

