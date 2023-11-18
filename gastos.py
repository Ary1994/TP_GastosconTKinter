import sqlite3
from tkinter import END
from tkinter import ttk
from tkinter import *

class GastosManager:
    vista_lista_gastos_frame = None  # Variable de clase para mantener la referencia a la ventana de lista de gastos
    def __init__(self,main_window):
        """
        Constructor de la clase GastosManager.
        
        Parámetros:
        - main_window: Referencia a la ventana principal de la aplicación.
        """
        self.conexion = sqlite3.connect("mi_basededatos.db") # Conexión a la base de datos
        self.main_window = main_window # Referencia a la ventana principal
        
    def agregar_gasto(self, nombre, cantidad, fecha, categoria):
        """
        Agrega un nuevo gasto a la base de datos.

        Parámetros:
        - nombre: Nombre del gasto.
        - cantidad: Monto del gasto.
        - fecha: Fecha del gasto.
        - categoria: Categoría del gasto.
        """

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
        """
        Obtiene la lista de todos los gastos almacenados en la base de datos y los muestra en un Listbox.

        Parámetros:
        - lista_gastos: Widget Listbox donde se mostrarán los gastos.

        """
        try:
            # Establece la conexión a la base de datos
            conexion = sqlite3.connect("mi_basededatos.db")
            cursor = conexion.cursor()

            # Consulta SQL para obtener los gastos
            cursor.execute("SELECT nombre, cantidad, fecha, categoria FROM gastos")
            gastos = cursor.fetchall()

            # Limpiar el Listbox antes de agregar nuevos datos
            lista_gastos.delete(0, END)
            aux=0
            # Agrega los gastos al Listbox en un formato específico
            for gasto in gastos:
                lista_gastos.insert(END, f" Fecha: {gasto[2]}, Cat: {gasto[3]},{gasto[0]} x {gasto[1]}")
                
            
            # Confirma los cambios en la base de datos
            conexion.commit()

        except sqlite3.Error as error:
            print("Error al obtener la lista de gastos:", error)
        finally:
            # Cierra la conexión a la base de datos de manera segura
            if conexion:
                conexion.close()

    def obtener_valores_y_agregar_gasto(self, nombre_entry, cantidad_entry, fecha_entry, categoria_combobox):
        """
        Obtiene los valores ingresados en los campos de entrada y el combobox
        para agregar un nuevo gasto a la base de datos.

        Parameters:
        - nombre_entry: Campo de entrada (Entry) que contiene el nombre del gasto.
        - cantidad_entry: Campo de entrada (Entry) que contiene el monto del gasto.
        - fecha_entry: Campo de entrada (Entry) que contiene la fecha del gasto.
        - categoria_combobox: Combobox que contiene la categoría del gasto.

        This method retrieves the values entered in the input fields and the combobox
        to add a new expense to the database.
        """
        # Obtiene los valores ingresados en los campos y el combobox
        nombre = nombre_entry.get()
        cantidad = float(cantidad_entry.get())
        fecha = fecha_entry.get()
        categoria = categoria_combobox.get()
        # Invoca al método para agregar un nuevo gasto con los valores obtenidos
        self.agregar_gasto(nombre, cantidad, fecha, categoria)

    def vista_lista_gastos(self, tree):
        """
        Actualiza la vista del Treeview con la lista de gastos desde la base de datos.

        Parameters:
        - tree: ttk.Treeview que representa la visualización de la lista de gastos.

        This method updates the Treeview's view with the list of expenses from the database.
        """
        # Borra todas las filas actuales del Treeview
        for item in tree.get_children():
            tree.delete(item)
        # Conecta con la base de datos y obtiene los datos de los gastos
        conn = sqlite3.connect("mi_basededatos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, cantidad, fecha, categoria FROM gastos ORDER BY id DESC")
        rows = cursor.fetchall()

        # Inserta cada gasto como una fila en el Treeview
        for row in rows:
            id_gasto, nombre_gasto, cantidad_gasto, fecha_gasto, categoria_gasto = row

            

            # Inserta los valores en el Treeview
            tree.insert("", "end", values=(id_gasto,nombre_gasto, cantidad_gasto, fecha_gasto, categoria_gasto, "", ""),
                        tags=("editable", "editable", "editable", "editable"))
            
        # Cierra la conexión a la base de datos
        conn.close()
    def filtrar_lista_gastos(self, lista_gastos_widget, fecha_filtro, categoria_filtro, nombre_filtro):
        """
        Filtra y muestra los gastos en el widget de lista de gastos basándose en los filtros aplicados.

        Parameters:
        - lista_gastos_widget: Widget (como un Listbox) para mostrar la lista de gastos filtrada.
        - fecha_filtro: Fecha utilizada como filtro para los gastos.
        - categoria_filtro: Categoría utilizada como filtro para los gastos.
        - nombre_filtro: Nombre utilizado como filtro para los gastos.

        This method filters and displays expenses in the list widget based on the applied filters.
        """
        try:
            conexion = sqlite3.connect("mi_basededatos.db")
            cursor = conexion.cursor()

            # Consulta SQL para obtener los gastos con filtrado
            consulta = "SELECT nombre, cantidad, fecha, categoria FROM gastos WHERE 1=1"

            if fecha_filtro:
                consulta += f" AND fecha = '{fecha_filtro}'"
            if categoria_filtro:
                consulta += f" AND categoria = '{categoria_filtro}'"
            if nombre_filtro:
                consulta += f" AND nombre = '{nombre_filtro}'"

            cursor.execute(consulta)
            gastos = cursor.fetchall()

            # Limpiar el Listbox antes de agregar nuevos datos
            lista_gastos_widget.delete(0, END)
            total_gasto=0
            # Agregar los gastos al Listbox
            for gasto in gastos:
                cantidad = gasto[1]
                total_gasto += cantidad

                lista_gastos_widget.insert(END, f"{gasto[0]} x {gasto[1]},\n Fecha: {gasto[2]}, Cat: {gasto[3]}")
            # Insertar el total de gastos al final de la lista
            lista_gastos_widget.insert(END, f"Gasto Total: {total_gasto}")
            conexion.commit()

        except sqlite3.Error as error:
            print("Error al obtener la lista de gastos:", error)
        finally:
            # Cierra la conexión a la base de datos, si está abierta
            if conexion:
                conexion.close()


    def eliminar_gasto(self, tree):
        """
        Elimina un gasto seleccionado de la base de datos y del Treeview.

        Parameters:
        - tree: Widget Treeview que muestra la lista de gastos.

        This method deletes a selected expense from the database and the Treeview widget.
         """
        selected_item = tree.selection()
        if selected_item:
            id_gasto = tree.item(selected_item, "values")[0]
            print("este es el id ",id_gasto)
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
                # Cierra la conexión a la base de datos, si está abierta
                if conexion:
                    conexion.close()


    def abrir_ventana_edicion(self, tree, selected_item):
        """
        Abre una ventana de edición para modificar los datos de un gasto seleccionado.

        Parameters:
        - tree: Widget Treeview que muestra la lista de gastos.
        - selected_item: Ítem seleccionado en el Treeview correspondiente al gasto a editar.

        This method opens an editing window to modify the data of a selected expense.
        """
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
        nuevo_nombre_entry.insert(0, item_values[1])
        nuevo_cantidad_entry.insert(0, item_values[2])
        nueva_fecha_entry.insert(0, item_values[3])
        categoria_combobox.set(item_values[4])
        # Agrega un botón para guardar los cambios
        guardar_cambios_button = Button(ventana_edicion, text="Guardar Cambios", command=lambda: self.guardar_cambios(tree, selected_item, nuevo_nombre_entry.get(), nuevo_cantidad_entry.get(), nueva_fecha_entry.get(), categoria_combobox.get()))
        guardar_cambios_button.pack()
  
    def guardar_cambios(self, tree, selected_item, nuevo_nombre, nuevo_cantidad, nueva_fecha,nueva_categoria):
        """
    Guarda los cambios realizados en los datos de un gasto y actualiza la base de datos y la vista.

    Parameters:
    - tree: Widget Treeview que muestra la lista de gastos.
    - selected_item: Ítem seleccionado en el Treeview correspondiente al gasto a editar.
    - nuevo_nombre: Nuevo nombre para el gasto.
    - nuevo_cantidad: Nuevo precio para el gasto.
    - nueva_fecha: Nueva fecha para el gasto.
    - nueva_categoria: Nueva categoría para el gasto.

    This method saves the changes made to an expense's data, updates the database, and refreshes the view.
    """
        id_gasto = tree.item(selected_item, "values")[0]

        try:
            conexion = sqlite3.connect("mi_basededatos.db")
            cursor = conexion.cursor()

            # Actualiza los datos del gasto en la base de datos
            cursor.execute("UPDATE gastos SET nombre=?, cantidad=?, fecha=? ,categoria =? WHERE id=?", (nuevo_nombre, nuevo_cantidad, nueva_fecha, nueva_categoria,id_gasto))
               
            # Confirma la transacción
            conexion.commit()

            # Actualiza la vista en el Treeview
            tree.item(selected_item, values=(id_gasto,nuevo_nombre, nuevo_cantidad, nueva_fecha, nueva_categoria))

            print(f"Gasto con ID {id_gasto} actualizado exitosamente.")
        except sqlite3.Error as error:
            print("Error al actualizar el gasto en la base de datos:", error)
        finally:
            # Cierra la conexión a la base de datos
            if conexion:
                conexion.close()
        

