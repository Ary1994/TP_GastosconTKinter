from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3

# Funciones
def agregar_gasto(nombre, cantidad, fecha, categoria):
    try:
        # Conectarse a la base de datos (o crearla si no existe)
        conexion = sqlite3.connect("mi_basededatos.db")
        cursor = conexion.cursor()

        # Crear una tabla si no existe
        cursor.execute("CREATE TABLE IF NOT EXISTS gastos (id INTEGER PRIMARY KEY,nombre TEXT,cantidad REAL, fecha TEXT,categoria TEXT)")

        # Insertar los datos del formulario en la tabla
        cursor.execute("INSERT INTO gastos (nombre, cantidad, fecha, categoria) VALUES (?, ?, ?, ?)",
                       (nombre, cantidad, fecha, categoria))

        # Confirmar la transacción
        conexion.commit()

        print("Gasto agregado exitosamente en la base de datos.")

    except sqlite3.Error as error:
        print("Error al agregar el gasto en la base de datos:", error)
    finally:
        # Cerrar la conexión a la base de datos
        if conexion:
            conexion.close()

def obtener_valores_y_agregar_gasto():
    nombre = nombre_entry.get()
    cantidad = float(cantidad_entry.get())
    fecha = fecha_entry.get()
    categoria = categoria_combobox.get()
    agregar_gasto(nombre, cantidad, fecha, categoria)

def obtener_lista_gastos():
    global lista_gastos
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

def vista_lista_gastos():
    global vista_lista_gastos_frame

    if vista_lista_gastos_frame is not None:
        vista_lista_gastos_frame.destroy()
    vista_lista_gastos_frame = Frame(pagina3, bg="lightblue")
    vista_lista_gastos_frame.pack()

    conn = sqlite3.connect("mi_basededatos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, cantidad, categoria FROM gastos ORDER BY id DESC")
    rows = cursor.fetchall()

    for row in rows:
        id_gasto, nombre_gasto, cantidad_gasto, categoria_gasto = row
        gasto_label = Label(vista_lista_gastos_frame, text=f"{nombre_gasto}: ${cantidad_gasto} - Categoría: {categoria_gasto}", bg="lightblue")

        editar_button = Button(vista_lista_gastos_frame, text="Editar", command=lambda id_gasto=id_gasto: editar_gasto(id_gasto))
        eliminar_button = Button(vista_lista_gastos_frame, text="Eliminar", command=lambda id_gasto=id_gasto: eliminar_gasto(id_gasto))

        gasto_label.grid(row=rows.index(row), column=0)
        editar_button.grid(row=rows.index(row), column=1)
        eliminar_button.grid(row=rows.index(row), column=2)

    conn.close()
def editar_gasto(gasto_id):
    global vista_lista_gastos_frame

    try:
        conexion = sqlite3.connect("mi_basededatos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, cantidad, fecha, categoria FROM gastos WHERE id = ?", (gasto_id,))
        gasto = cursor.fetchone()

        if gasto:
            nombre, cantidad, fecha, categoria = gasto

            # Crear y configurar los elementos de edición
            editar_frame = Frame(vista_lista_gastos_frame, bg="lightblue")
            editar_frame.grid(row=gasto_id, column=0, columnspan=3, sticky="ew")  # El parámetro sticky asegura que se extienda horizontalmente

            nombre_label = Label(editar_frame, text="Nombre:", bg='lightblue')
            nombre_label.grid(row=0, column=0)
            nombre_entry = Entry(editar_frame)
            nombre_entry.grid(row=0, column=1)
            nombre_entry.insert(0, nombre)

            cantidad_label = Label(editar_frame, text="Cantidad:", bg='lightblue')
            cantidad_label.grid(row=1, column=0)
            cantidad_entry = Entry(editar_frame)
            cantidad_entry.grid(row=1, column=1)
            cantidad_entry.insert(0, cantidad)

            fecha_label = Label(editar_frame, text="Fecha:", bg='lightblue')
            fecha_label.grid(row=2, column=0)
            fecha_entry = Entry(editar_frame)
            fecha_entry.grid(row=2, column=1)
            fecha_entry.insert(0, fecha)

            categoria_label = Label(editar_frame, text="Categoría:", bg='lightblue')
            categoria_label.grid(row=3, column=0)
            categorias = ["Alimentos", "Transporte", "Entretenimiento", "Salud", "Otros"]
            categoria_combobox = ttk.Combobox(editar_frame, values=categorias)
            categoria_combobox.grid(row=3, column=1)
            categoria_combobox.set(categoria)

            # Crear un botón para guardar cambios y asociarlo a la función guardar_cambios
            guardar_button = Button(editar_frame, text="Guardar Cambios", command=lambda: guardar_cambios(gasto_id, nombre_entry, cantidad_entry, fecha_entry, categoria_combobox))
            guardar_button.grid(row=4, column=0, columnspan=2, pady=10)  # Agrega espacio entre el botón y los campos de edición

    except sqlite3.Error as error:
        print("Error al editar el gasto:", error)

def guardar_cambios(gasto_id, nombre_entry, cantidad_entry, fecha_entry, categoria_combobox):
    nuevo_nombre = nombre_entry.get()
    nuevo_cantidad = float(cantidad_entry.get())
    nueva_fecha = fecha_entry.get()
    nueva_categoria = categoria_combobox.get()

    try:
        conexion = sqlite3.connect("mi_basededatos.db")
        cursor = conexion.cursor()
        cursor.execute("UPDATE gastos SET nombre = ?, cantidad = ?, fecha = ?, categoria = ? WHERE id = ?", (nuevo_nombre, nuevo_cantidad, nueva_fecha, nueva_categoria, gasto_id))
        conexion.commit()
        conexion.close()

        vista_lista_gastos()  # Actualizar la lista de gastos en la interfaz después de guardar los cambios

    except sqlite3.Error as error:
        print("Error al guardar los cambios:", error)

def eliminar_gasto(gasto_id):
    global vista_lista_gastos_frame

    # Obtener el ID del gasto seleccionado
    print(gasto_id)

    try:
        conexion = sqlite3.connect("mi_basededatos.db")
        cursor = conexion.cursor()

        # Eliminar el gasto de la base de datos
        cursor.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))

        conexion.commit()
        conexion.close()

        vista_lista_gastos()  # Actualizar la lista de gastos en la interfaz


    except sqlite3.Error as error:
        print("Error al eliminar el gasto de la base de datos:", error)
#variables globales
vista_lista_gastos_frame = None

ventana1 = Tk()
ventana1.title("Registro Gastos")

# Cargar la imagen de fondo y redimensionarla
imagen_fondo = Image.open("libreta.jpg")
ancho_imagen, alto_imagen =1000, 1000  # Tamaño deseado

# Redimensionar la imagen con interpolación suave (ANTIALIAS)
imagen_fondo.thumbnail((ancho_imagen, alto_imagen),Image.BILINEAR)
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
# Obtenemos las dimensiones de la imagen de fondo
ancho_imagen = imagen_fondo.width()
alto_imagen = imagen_fondo.height()

# Ajustamos el tamaño de la ventana a las dimensiones de la imagen
ventana1.geometry(f"{ancho_imagen}x{alto_imagen}")

# Incluimos panel para pestañas
cuaderno1 = ttk.Notebook(ventana1)
cuaderno1.pack(fill="both", expand="yes")

# Creamos las pestañas
pagina1 = Frame(cuaderno1)
pagina2 = Frame(cuaderno1)
pagina3 = Frame(cuaderno1)
pagina4 = Frame(cuaderno1)
pagina2.configure(bg="lightblue")
pagina3.configure(bg="lightblue")
# Agregamos pestañas creadas
cuaderno1.add(pagina1, text="Registrar Gtos")
cuaderno1.add(pagina2, text="Resumen Gtos")
cuaderno1.add(pagina3, text="Editar Gtos")
cuaderno1.add(pagina4, text="Descargar ")

# Configurar la imagen de fondo en las pestañas
fondo_label = Label(pagina1, image=imagen_fondo)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

fondo_label = Label(pagina4, image=imagen_fondo)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

# Elementos Pestaña 1
titulo_label = Label(pagina1, text="Registro de Gasto", font=("Helvetica", 14), bg='lightblue', relief='solid')
titulo_label.pack(pady=10)  # Espacio entre el título y los campos

nombre_label = Label(pagina1, text="Nombre del gasto:", bg='lightblue')
nombre_label.pack()
nombre_entry = Entry(pagina1)
nombre_entry.pack()

cantidad_label = Label(pagina1, text="Precio:", bg='lightblue')
cantidad_label.pack()
cantidad_entry = Entry(pagina1)
cantidad_entry.pack()

fecha_label = Label(pagina1, text="Fecha:", bg='lightblue')
fecha_label.pack()
fecha_entry = Entry(pagina1)
fecha_entry.pack()

categoria_label = Label(pagina1, text="Categoría:", bg='lightblue')
categoria_label.pack()
categorias = ["Alimentos", "Transporte", "Entretenimiento", "Salud", "Otros"]
categoria_combobox = ttk.Combobox(pagina1, values=categorias)
categoria_combobox.pack()

# Botón para agregar gasto en el formulario
agregar_button = Button(pagina1, text="Agregar Gasto", command=obtener_valores_y_agregar_gasto)
agregar_button.pack()

# Elementos página 2
lista_gastos_label = Label(pagina2, text="Lista de Gastos Generales", bg='lightblue')
lista_gastos_label.pack(pady=10)

lista_gastos = Listbox(pagina2, bg='lightblue',width=50)
lista_gastos.pack()

# Botón para obtener la lista de gastos
obtener_lista_button = Button(pagina2, text="Obtener Lista de Gastos", command=obtener_lista_gastos)
obtener_lista_button.pack()


# Elementos página 3
obtener_lista_button = Button(pagina3, text="Obtener Lista de Gastos", command=vista_lista_gastos)
obtener_lista_button.pack()

# Main loop
ventana1.mainloop()
