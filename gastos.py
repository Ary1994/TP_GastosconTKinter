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

    def obtener_valores_y_agregar_gasto(self, nombre_entry, cantidad_entry, fecha_entry, categoria_combobox):
        nombre = nombre_entry.get()
        cantidad = float(cantidad_entry.get())
        fecha = fecha_entry.get()
        categoria = categoria_combobox.get()
        self.agregar_gasto(nombre, cantidad, fecha, categoria)

    def vista_lista_gastos(self, tree):
        # Borra la tabla antes de insertar nuevos registros
        for item in tree.get_children():
            tree.delete(item)

        conn = sqlite3.connect("mi_basededatos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, cantidad, fecha, categoria FROM gastos ORDER BY id DESC")
        rows = cursor.fetchall()

        for row in rows:
            id_gasto, nombre_gasto, cantidad_gasto, fecha_gasto, categoria_gasto = row

            

            # Inserta los botones como valores en el ttk.Treeview
            tree.insert("", "end", values=(nombre_gasto, cantidad_gasto, fecha_gasto, categoria_gasto, "", ""),
                        tags=("editable", "editable", "editable", "editable"))

        conn.close()

    def editar_gasto(self, tree):
            selected_item = tree.selection()
            if selected_item:
                id_gasto = tree.item(selected_item, "values")[-1]
                # Aquí debes implementar la lógica para la edición del gasto con el ID id_gasto


    def eliminar_gasto(self, tree):

        selected_item = tree.selection()
        if selected_item:
            id_gasto = tree.item(selected_item, "values")[-1]

            try:
                conexion = sqlite3.connect("mi_basededatos.db")
                cursor = conexion.cursor()

                # Elimina el registro de gasto en la base de datos usando el ID
                cursor.execute("DELETE FROM gastos WHERE id=?", (id_gasto,))

                # Confirma la transacción
                conexion.commit()

                # Elimina la fila seleccionada del Treeview
                tree.delete(selected_item)

                print(f"Gasto con ID {id_gasto} eliminado exitosamente.")
            except sqlite3.Error as error:
                print("Error al eliminar el gasto en la base de datos:", error)
            finally:
                if conexion:
                    conexion.close()


    def abrir_ventana_edicion(self, tree, selected_item):
        ventana_edicion = Toplevel(self.main_window.root)
        ventana_edicion.title("Editar Gasto")
        ventana_edicion.iconbitmap('notebook.ico')
        ventana_edicion.configure(bg="lightblue")

        # Agrega etiquetas y campos de entrada para editar los datos
        nombre_label = Label(ventana_edicion, text="Nuevo Nombre del gasto:", bg='lightblue')
        nombre_label.pack()
        nuevo_nombre_entry = Entry(ventana_edicion)
        nuevo_nombre_entry.pack()

        cantidad_label = Label(ventana_edicion, text="Nuevo Precio:", bg='lightblue')
        cantidad_label.pack()
        nuevo_cantidad_entry = Entry(ventana_edicion)
        nuevo_cantidad_entry.pack()

        fecha_label = Label(ventana_edicion, text="Nueva Fecha:", bg='lightblue')
        fecha_label.pack()
        nueva_fecha_entry = Entry(ventana_edicion)
        nueva_fecha_entry.pack()
        categoria_label = Label( ventana_edicion,text="Categoría:", bg='lightblue')
        categoria_label.pack()
        categorias = ["Alimentos", "Transporte", "Entretenimiento", "Salud", "Otros"]
        categoria_combobox = ttk.Combobox(ventana_edicion, values=categorias)
        categoria_combobox.pack()

        # Obtén los datos actuales del gasto seleccionado
        item = tree.item(selected_item)
        item_values = item["values"]
        nuevo_nombre_entry.insert(0, item_values[0])
        nuevo_cantidad_entry.insert(0, item_values[1])
        nueva_fecha_entry.insert(0, item_values[2])
        categoria_combobox.set(item_values[3])
        # Agrega un botón para guardar los cambios
        guardar_cambios_button = Button(ventana_edicion, text="Guardar Cambios", command=lambda: self.guardar_cambios(tree, selected_item, nuevo_nombre_entry.get(), nuevo_cantidad_entry.get(), nueva_fecha_entry.get(), categoria_combobox.get()))
        guardar_cambios_button.pack()
  
    def guardar_cambios(self, tree, selected_item, nuevo_nombre, nuevo_cantidad, nueva_fecha,nueva_categoria):
        id_gasto = tree.item(selected_item, "values")[-1]

        try:
            conexion = sqlite3.connect("mi_basededatos.db")
            cursor = conexion.cursor()

            # Actualiza los datos del gasto en la base de datos
            cursor.execute("UPDATE gastos SET nombre=?, cantidad=?, fecha=? ,categoria =? WHERE id=?", (nuevo_nombre, nuevo_cantidad, nueva_fecha, nueva_categoria,id_gasto))
               
            # Confirma la transacción
            conexion.commit()

            # Actualiza la vista en el Treeview
            tree.item(selected_item, values=(nuevo_nombre, nuevo_cantidad, nueva_fecha, nueva_categoria,id_gasto))

            print(f"Gasto con ID {id_gasto} actualizado exitosamente.")
        except sqlite3.Error as error:
            print("Error al actualizar el gasto en la base de datos:", error)
        finally:
            if conexion:
                conexion.close()
        

