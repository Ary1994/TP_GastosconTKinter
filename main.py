from tkinter import *
from tkinter import ttk
from gui import MainWindow

if __name__ == "__main__":
    # Crea la ventana principal de la aplicación
    root = Tk()
    # Instancia la clase MainWindow y la asocia a la ventana principal
    app = MainWindow(root)
    # Inicia el bucle principal para la interfaz de usuario
    root.mainloop()
