##codigo simple para ver las fuentes del sistema y elegir más fácil cual poner en la app
import tkinter as tk
import tkinter.font as font

def show_fonts():
    root = tk.Tk()
    root.title("Fuentes Disponibles")

    # Crear un Canvas para el scroll
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Crear un scrollbar y asociarlo con el canvas
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configurar el canvas para trabajar con el scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un frame que contenga las etiquetas de las fuentes
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Obtener todas las fuentes disponibles
    fonts = list(font.families())

    # Mostrar las fuentes en el frame
    for f in fonts:
        label = tk.Label(frame, text=f, font=(f, 12))
        label.pack()

    # Actualizar el tamaño del canvas cuando se agreguen etiquetas
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Agregar una etiqueta para las instrucciones
    instructions = tk.Label(root, text="Esta es la lista de fuentes disponibles en tu sistema:")
    instructions.pack()

    # Ejecutar la ventana
    root.mainloop()

# Llamar a la función para mostrar las fuentes
show_fonts()
