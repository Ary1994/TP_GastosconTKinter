from tkinter import ttk
from tkinter import *
from gastos import GastosManager

class MainWindow:
    def __init__(self, root):

        self.root = root
        self.root.title("Registro Gastos")
        self.root.iconbitmap('notebook.ico')
        self.cuaderno = ttk.Notebook(self.root)
        self.cuaderno.pack(fill="both", expand="yes")
        

        self.page1 = Frame(self.cuaderno)
        self.page2 = Frame(self.cuaderno)
        self.page3 = Frame(self.cuaderno)
        
        self.cuaderno.add(self.page1, text="Registrar Gastos")
        self.cuaderno.add(self.page2, text="Resumen Gastos")
        self.cuaderno.add(self.page3, text="Editar Gastos")

        self.gastos_manager = GastosManager(self)


        self.page1.configure(bg="lightblue")
        self.page2.configure(bg="lightblue")
        self.page3.configure(bg="lightblue")

        self.init_page1()
        self.init_page2()
        self.init_page3()

    def init_page1(self):
       
        titulo_label = Label(self.page1,text="Registro de Gasto", font=("Helvetica", 14), bg='lightblue', relief='solid')
        titulo_label.pack(pady=10)  # Espacio entre el título y los campos

        nombre_label = Label(self.page1, text="Nombre del gasto:", bg='lightblue')
        nombre_label.pack()
        nombre_entry = Entry(self.page1)
        nombre_entry.pack()

        cantidad_label = Label(self.page1, text="Precio:", bg='lightblue')
        cantidad_label.pack()
        cantidad_entry = Entry(self.page1)
        cantidad_entry.pack()

        fecha_label = Label(self.page1, text="Fecha:", bg='lightblue')
        fecha_label.pack()
        fecha_entry = Entry(self.page1)
        fecha_entry.pack()

        categoria_label = Label( self.page1,text="Categoría:", bg='lightblue')
        categoria_label.pack()
        categorias = ["Alimentos", "Transporte", "Entretenimiento", "Salud", "Otros"]
        categoria_combobox = ttk.Combobox(self.page1, values=categorias)
        categoria_combobox.pack()

        # Botón para agregar gasto en el formulario
        agregar_button = Button( self.page1 ,text="Agregar Gasto", command=lambda: self.gastos_manager.obtener_valores_y_agregar_gasto(nombre_entry, cantidad_entry, fecha_entry, categoria_combobox))
        agregar_button.pack()

    def init_page2(self):
        
        lista_gastos_label = Label(self.page2,text="Lista de Gastos Generales", bg='lightblue')
        lista_gastos_label.pack(pady=10)

        lista_gastos = Listbox(self.page2, bg='lightblue',width=50)
        lista_gastos.pack()

        obtener_lista_button = Button(self.page2,text="Obtener Lista de Gastos",command=lambda: self.gastos_manager.obtener_lista_gastos(lista_gastos))
        obtener_lista_button.pack()
    
    def init_page3(self):
        lista_gastos_label = Label(self.page3,text="Editar gastos ", bg='lightblue')
        lista_gastos_label.pack(pady=10)
        columns = ("Nombre", "Precio", "Fecha", "Categoría")
        tree = ttk.Treeview(self.page3, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack()
        obtener_lista_button = Button(self.page3, text="Obtener Lista de Gastos", command=lambda: self.gastos_manager.vista_lista_gastos(tree))
        obtener_lista_button.pack()
        editar_button = Button(self.page3, text="Editar Gasto", command=lambda: self.gastos_manager.editar_gasto(tree))
        editar_button.pack()

        eliminar_button = Button(self.page3, text="Eliminar Gasto", command=lambda: self.gastos_manager.eliminar_gasto(tree))
        eliminar_button.pack()

 

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    gastos_manager = GastosManager(app)  # Pasa la referencia de MainWindow a GastosManager
    root.mainloop()
