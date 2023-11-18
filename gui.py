from tkinter import ttk
from tkinter import *
from gastos import GastosManager
from tkinter import colorchooser
class MainWindow:
    """Clase que define la interfaz gráfica principal."""
    def __init__(self, root):
        """Inicializa la ventana principal y las pestañas."""
        self.root = root
        self.root.title("Registro Gastos")
        self.root.iconbitmap('notebook.ico')
        self.cuaderno = ttk.Notebook(self.root)
        self.cuaderno.pack(fill="both", expand="yes")
        
        # Creación de las pestañas

        self.page1 = Frame(self.cuaderno)
        self.page2 = Frame(self.cuaderno)
        self.page3 = Frame(self.cuaderno)
        self.page4 = Frame(self.cuaderno)

        # Agrega las pestañas al Notebook con sus respectivos nombres

        self.cuaderno.add(self.page1, text="Registrar Gastos")
        self.cuaderno.add(self.page2, text="Resumen Gastos")
        self.cuaderno.add(self.page3, text="Modificar Gastos")

        # Crea una instancia de GastosManager para gestionar los gastos
        self.gastos_manager = GastosManager(self)
        self.cuaderno.add(self.page4,text="Cambar color")

        # Configuración de colores de las pestañas
        self.page1.configure(bg="lightblue")
        self.page2.configure(bg="lightblue")
        self.page3.configure(bg="lightblue")
        self.page4.configure(bg="lightblue")

        # Inicialización de las páginas individuales
        self.init_page1()
        self.init_page2()
        self.init_page3()
        self.init_page4()
    hex_color = "#FFFFFF" # Variable para almacenar el color seleccionado
    def cambiar_color_fondo(self):
        """Permite cambiar el color de fondo de las pestañas."""
        color, _ = colorchooser.askcolor(title="Seleccionar un color de fondo")
        
        self.hex_color = '#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))
        # Cambia el color de fondo de las pestañas
        if color:
            self.page1.configure(bg=self.hex_color)
            self.page2.configure(bg=self.hex_color)
            self.page3.configure(bg=self.hex_color)
            self.page4.configure(bg=self.hex_color)

    def init_page4(self):
        """Inicializa la pestaña 'Cambiar color'."""
        # Botón para cambiar el color de fondo
        cambiar_color_button = Button(self.page4, text="Cambiar Color de Fondo", command=self.cambiar_color_fondo)
        cambiar_color_button.pack()
        cambiar_color_button.pack(pady=20)  # Espacio vertical entre el botón y el borde superior
        cambiar_color_button.pack(padx=20, anchor="center")  # Centrar horizontalmente y espacio lateral

    
    def init_page1(self):
        """Inicializa la pestaña 'Registrar Gasto'."""
        titulo_label = Label(self.page1,text="Registro de Gasto", font=("Helvetica", 14),  relief='solid')
      # Espacio entre el título y los campos
        titulo_label.pack(pady=10)  # Espacio entre el título y los campos
        # Etiquetas y campos de entrada para nombre, cantidad, fecha y categoría
        nombre_label = Label(self.page1, text="Nombre del gasto:",bg=self.hex_color) 
        nombre_label.pack()
        nombre_entry = Entry(self.page1)# Campo de entrada para el nombre del gasto
        nombre_entry.pack()

        cantidad_label = Label(self.page1, text="Precio:", )
        cantidad_label.pack()
        cantidad_entry = Entry(self.page1)# Campo de entrada para la cantidad del gasto
        cantidad_entry.pack()

        fecha_label = Label(self.page1, text="Fecha:", )
        fecha_label.pack()
        fecha_entry = Entry(self.page1)# Campo de entrada para la fecha del gasto
        fecha_entry.pack()

        categoria_label = Label( self.page1,text="Categoría:",) 
        categoria_label.pack()
        categorias = ["Alimentos", "Transporte", "Entretenimiento", "Salud", "Otros"]
        categoria_combobox = ttk.Combobox(self.page1, values=categorias)# Combobox para seleccionar la categoría
        categoria_combobox.pack()

        # Botón para agregar gasto en el formulario
        agregar_button = Button( self.page1 ,text="Agregar Gasto", command=lambda: self.gastos_manager.obtener_valores_y_agregar_gasto(nombre_entry, cantidad_entry, fecha_entry, categoria_combobox))
        agregar_button.pack()

    def init_page2(self):
        """Inicializa la pestaña 'Resumen Gastos'."""
        # Título y separación
        lista_gastos_label = Label(self.page2,text="Lista de Gastos Generales", font=("Helvetica", 14),  relief='solid')
        lista_gastos_label.pack(pady=10)# Espacio entre el título y los elementos

        # Crear los widgets de filtrado
        filtro_frame = Frame(self.page2, )# Marco para los elementos de filtrado
        filtro_frame.pack()

        # Etiquetas y campos de entrada para filtrar por fecha, categoría y nombre
        filtro_label = Label(filtro_frame, text="Filtrar por:", )
        filtro_label.grid(row=0, column=0)

        fecha_label = Label(filtro_frame, text="Fecha:", )
        fecha_label.grid(row=0, column=1)
        fecha_entry = Entry(filtro_frame)# Campo de entrada para filtrar por fecha
        fecha_entry.grid(row=0, column=2)

        categoria_label = Label(filtro_frame, text="Categoría:", )
        categoria_label.grid(row=0, column=3)
        categorias = ["", "Alimentos", "Transporte", "Entretenimiento", "Salud", "Otros"]
        categoria_combobox = ttk.Combobox(filtro_frame, values=categorias)# Combobox para filtrar por categoría
        categoria_combobox.grid(row=0, column=4)

        nombre_label = Label(filtro_frame, text="Nombre:", )
        nombre_label.grid(row=0, column=5)
        nombre_entry = Entry(filtro_frame)# Campo de entrada para filtrar por nombre
        nombre_entry.grid(row=0, column=6)

        # Botón para aplicar el filtro a la lista de gastos
        aplicar_filtro_button = Button(filtro_frame, text="Aplicar Filtro",
                                command=lambda: self.gastos_manager.filtrar_lista_gastos(lista_gastos, fecha_entry.get(), categoria_combobox.get(), nombre_entry.get()))
        aplicar_filtro_button.grid(row=0, column=7)

        # Lista de gastos
        lista_gastos = Listbox(self.page2,  width=50)# Lista para mostrar los gastos filtrados
        lista_gastos.pack()

        # Botón para obtener todos los gastos sin filtros
        obtener_lista_button = Button(self.page2, text="Obtener Todos los Gastos",
                                command=lambda: self.gastos_manager.obtener_lista_gastos(lista_gastos))
        obtener_lista_button.pack()
    
    def init_page3(self):
        
        """Inicializa la pestaña 'Modificar gastos'."""
        # Etiqueta de título y configuración de la tabla
        lista_gastos_label = Label(self.page3,text="Modificar gastos", font=("Helvetica", 14),  relief='solid')
        lista_gastos_label.pack(pady=10)# Espacio entre el título y los elementos
        columns = ("ID","Nombre", "Precio", "Fecha", "Categoría")
        tree = ttk.Treeview(self.page3, columns=columns, show="headings")# Configuración del Treeview para mostrar los gastos
        for col in columns:
            tree.heading(col, text=col)# Encabezados de columnas
            tree.column(col, width=100)# Ancho de columnas
        tree.pack()# Mostrar el Treeview en la interfaz
        # Botones para editar, eliminar y obtener la lista de gastos
        editar_button = Button(self.page3, text="Editar Gasto", command=lambda: self.gastos_manager.abrir_ventana_edicion(tree, tree.selection()[0]))
        eliminar_button = Button(self.page3, text="Eliminar Gasto", command=lambda: self.gastos_manager.eliminar_gasto(tree))

        # Botón para obtener la lista de gastos
        obtener_lista_button = Button(self.page3, text="Obtener Lista de Gastos", command=lambda: (self.gastos_manager.vista_lista_gastos(tree), obtener_lista_button.pack_forget(), editar_button.pack(side="left"), eliminar_button.pack(side="right")))
        obtener_lista_button.pack() # Agregar botón 'Obtener Lista de Gastos' a la interfaz

   



 

if __name__ == "__main__":
    # Crea una ventana principal, instancia la clase MainWindow y el gestor de gastos, y ejecuta la GUI
    
    root = Tk()
    app = MainWindow(root)
    gastos_manager = GastosManager(app)  # Pasa la referencia de MainWindow a GastosManager
    root.mainloop()
