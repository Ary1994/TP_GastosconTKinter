import tkinter as tk
from tkinter import ttk
import sqlite3
import threading

# Variable global para lista_gastos
lista_gastos = None
boton_filtrar = None

def conectar_base_datos():
    # Conecta a la base de datos (o la crea si no existe)
    conn = sqlite3.connect("gastos.db")

    # Crea una tabla llamada "gastos" si no existe
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            cantidad REAL NOT NULL,
            categoria TEXT
        )
    ''')

    # Guarda los cambios y cierra la conexión a la base de datos
    conn.commit()
    conn.close()

def vista_form():
    # Ocultar otras vistas
    ocultar_vistas()
    
    formulario_frame.pack()
    nombre_label.pack()
    nombre_entry.pack()
    cantidad_label.pack()
    cantidad_entry.pack()
    categoria_label.pack()
    categoria_combobox.pack()
    agregar_button.pack()
    
    # Mostrar el contenedor de formulario

def obtener_lista_gastos():
    # Borrar la lista actual de gastos en la interfaz
    lista_gastos.delete(0, tk.END)
    
    # Definir una función para realizar la consulta en un hilo separado
    def consulta_db():
        conn = sqlite3.connect("gastos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, cantidad, categoria FROM gastos")
        rows = cursor.fetchall()
        conn.close()
        
        # Actualizar la lista de gastos en la interfaz
        for row in rows:
            nombre_gasto, cantidad_gasto, categoria_gasto = row
            lista_gastos.insert(tk.END, f"{nombre_gasto}: ${cantidad_gasto} - Categoría: {categoria_gasto}")
    
    # Crear un hilo para la consulta y ejecutarlo
    consulta_thread = threading.Thread(target=consulta_db)
    consulta_thread.start()

def cargar_gastos():
    # Ocultar otras vistas
    ocultar_vistas()
    boton_filtrar = tk.Button(root, text="Filtrar por Categoría",)
    
    boton_filtrar.pack()
    lista_gastos.pack()
    obtener_lista_gastos()  # Mostrar todos los gastos

def agregar_gasto():
    nombre_gasto = nombre_entry.get()
    cantidad_gasto = cantidad_entry.get()
    categoria_gasto = categoria_combobox.get()
    
    if nombre_gasto and cantidad_gasto:
        obtener_lista_gastos()  # Actualizar la lista de gastos
        nombre_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        
        # Agregar el gasto a la base de datos
        conn = sqlite3.connect("gastos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO gastos (nombre, cantidad, categoria) VALUES (?, ?, ?)", (nombre_gasto, cantidad_gasto, categoria_gasto))
        conn.commit()
        conn.close()

def ocultar_vistas():
    vistas = [formulario_frame, vista_lista_gastos_frame, lista_gastos, vista_filtrar_categoria_frame]

    # Oculta todas las vistas en la lista
    for vista in vistas:
        if vista:
            vista.pack_forget()

vista_lista_gastos_frame = None

def filtrar_gastos_por_categoria():
    # Borrar la lista actual de gastos en la interfaz
    lista_gastos.delete(0, tk.END)
    
    # Obtener la categoría seleccionada del filtro
    categoria_seleccionada = categoria_combobox_filtrar.get()
    
    # Definir una función para realizar la consulta en un hilo separado
    def consulta_db():
        conn = sqlite3.connect("gastos.db")
        cursor = conn.cursor()
        
        if categoria_seleccionada == "Todas":
            cursor.execute("SELECT nombre, cantidad, categoria FROM gastos")
        else:
            cursor.execute("SELECT nombre, cantidad, categoria FROM gastos WHERE categoria=?", (categoria_seleccionada,))
            
        rows = cursor.fetchall()
        conn.close()
        
        # Actualizar la lista de gastos en la interfaz
        for row in rows:
            nombre_gasto, cantidad_gasto, categoria_gasto = row
            lista_gastos.insert(tk.END, f"{nombre_gasto}: ${cantidad_gasto} - Categoría: {categoria_gasto}")
    
    # Crear un hilo para la consulta y ejecutarlo
    consulta_thread = threading.Thread(target=consulta_db)
    consulta_thread.start()

def vista_lista_gastos():
    global vista_lista_gastos_frame
    
    # Ocultar otras vistas
    ocultar_vistas()

    # Crear un marco para la lista de gastos
    if vista_lista_gastos_frame is None:
        vista_lista_gastos_frame = tk.Frame(root)
        vista_lista_gastos_frame.pack()

        # Obtener la lista de gastos desde la base de datos
        conn = sqlite3.connect("gastos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, cantidad, categoria FROM gastos")
        rows = cursor.fetchall()

        # Mostrar los gastos en la lista de la interfaz con botón de edición
        for row in rows:
            id_gasto, nombre_gasto, cantidad_gasto, categoria_gasto = row
            gasto_label = tk.Label(vista_lista_gastos_frame, text=f"{nombre_gasto}: ${cantidad_gasto} - Categoría: {categoria_gasto}")
            editar_button = tk.Button(vista_lista_gastos_frame, text="Editar", command=lambda id_gasto=id_gasto: editar_gasto(id_gasto))

            gasto_label.grid(row=id_gasto, column=0)  # Coloca el label en la columna 0
            editar_button.grid(row=id_gasto, column=1)  # Coloca el botón en la columna 1

        conn.close()

    # Guardar el marco contenedor en una variable global
    vista_lista_gastos_frame = vista_lista_gastos_frame

# Configurar la ventana principal
root = tk.Tk()
root.title("App de Gastos")
root.geometry("500x400")

# Menús
menu = tk.Menu(root)
root.config(menu=menu)
archivo_menu = tk.Menu(menu)
menu.add_cascade(label="Menu", menu=archivo_menu)
archivo_menu.add_command(label="Registrar Gastos", command=vista_form)
archivo_menu.add_command(label="Resumen Gastos", command=cargar_gastos)
archivo_menu.add_command(label="Editar Gastos", command=vista_lista_gastos)
archivo_menu.add_command(label="Descargar Resumen")
archivo_menu.add_separator()
archivo_menu.add_command(label="Salir", command=root.quit)

# Contenedor para el formulario
formulario_frame = tk.Frame(root)

# Etiquetas y entradas de texto en el formulario
nombre_label = tk.Label(formulario_frame, text="Nombre del gasto:")
nombre_entry = tk.Entry(formulario_frame)
cantidad_label = tk.Label(formulario_frame, text="Precio:")
cantidad_entry = tk.Entry(formulario_frame)
categoria_label = tk.Label(formulario_frame, text="Categoría:")
categorias = ["Alimentos", "Transporte", "Entretenimiento", "Salud", "Otros"]
categoria_combobox = ttk.Combobox(formulario_frame, values=categorias)

# Botón para agregar gasto en el formulario
agregar_button = tk.Button(formulario_frame, text="Agregar Gasto", command=agregar_gasto)

# Lista de gastos
lista_gastos = tk.Listbox(root, width=40)

# Etiqueta y combobox para seleccionar la categoría de filtro
categoria_label_filtrar = tk.Label(root, text="Seleccionar Categoría:")
categorias_filtrar = ["Todas"] + categorias
categoria_combobox_filtrar = ttk.Combobox(root, values=categorias_filtrar)
categoria_combobox_filtrar.set("Todas")  # Establece el valor predeterminado en "Todas"



# Frame para la vista de filtrar por categoría
vista_filtrar_categoria_frame = tk.Frame(root)

# Ejecutar la aplicación
conectar_base_datos()  # Llama a esta función para asegurarte de que la base de datos esté creada
root.mainloop()
