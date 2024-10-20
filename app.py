import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
import datetime
import os
import matplotlib.pyplot as plt

# Archivo donde guardaremos las categorías
CATEGORIES_FILE = "categories.json"

# Cargar categorías desde el archivo JSON
def load_categories():
    if os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, "r") as file:
            return json.load(file)
    return ["Salud", "Trabajo", "Ocio", "Personal", "Estudio"]  # Categorías por defecto

# Guardar categorías en el archivo JSON
def save_categories():
    with open(CATEGORIES_FILE, "w") as file:
        json.dump(categories, file)


def update_category_menu():
    category_menu['menu'].delete(0, 'end')  # Limpia el menú existente
    for category in categories:
        category_menu['menu'].add_command(label=category, command=lambda value=category: category_var.set(value))
    category_var.set(categories[0])  # Restablecer la categoría seleccionada

def edit_categories():
    edit_window = tk.Toplevel(root)
    edit_window.title("Editar Categorías")

    # Listbox para mostrar las categorías actuales
    category_listbox = tk.Listbox(edit_window)
    category_listbox.pack(pady=10)
    
    for category in categories:
        category_listbox.insert(tk.END, category)

    def add_new_category():
        new_category = simpledialog.askstring("Nueva categoría", "Introduce el nombre de la nueva categoría:")
        if new_category:
            if new_category not in categories:
                categories.append(new_category)
                save_categories()
                update_category_menu()
                category_listbox.insert(tk.END, new_category)
                messagebox.showinfo("Éxito", f"Categoría '{new_category}' agregada.")
            else:
                messagebox.showwarning("Advertencia", "La categoría ya existe.")

    def modify_category():
        selected_index = category_listbox.curselection()
        if selected_index:
            current_category = categories[selected_index[0]]
            new_name = simpledialog.askstring("Modificar categoría", f"Modificar '{current_category}':")
            if new_name and new_name != current_category:
                if new_name not in categories:
                    categories[selected_index[0]] = new_name
                    save_categories()
                    update_category_menu()
                    category_listbox.delete(selected_index)
                    category_listbox.insert(selected_index, new_name)
                    messagebox.showinfo("Éxito", "Categoría modificada.")
                else:
                    messagebox.showwarning("Advertencia", "La nueva categoría ya existe.")
        else:
            messagebox.showerror("Error", "Por favor, selecciona una categoría para modificar.")

    def delete_category():
        selected_index = category_listbox.curselection()
        if selected_index:
            category_to_delete = categories[selected_index[0]]
            if category_to_delete != "Personal":
                categories.remove(category_to_delete)
                save_categories()
                update_category_menu()
                category_listbox.delete(selected_index)
                messagebox.showinfo("Éxito", f"Categoría '{category_to_delete}' eliminada.")
            else:
                messagebox.showwarning("Advertencia", "No se puede eliminar la categoría por defecto.")
        else:
            messagebox.showerror("Error", "Por favor, selecciona una categoría para eliminar.")

    # Botones para añadir, modificar y eliminar categorías
    tk.Button(edit_window, text="Añadir Categoría", command=add_new_category).pack(pady=5)
    tk.Button(edit_window, text="Modificar Categoría", command=modify_category).pack(pady=5)
    tk.Button(edit_window, text="Eliminar Categoría", command=delete_category).pack(pady=5)



# Archivo donde guardaremos los hábitos
HABITS_FILE = "habits.json"

# Cargar hábitos desde el archivo JSON
def load_habits():
    if os.path.exists(HABITS_FILE):
        with open(HABITS_FILE, "r") as file:
            return json.load(file)
    return []

# Guardar hábitos en el archivo JSON
def save_habits():
    with open(HABITS_FILE, "w") as file:
        json.dump(habits, file, default=str)

# Función para agregar un nuevo hábito
def add_habit():
    habit_name = habit_entry.get()
    category = category_var.get()
    if habit_name:
        habit = {
            "name": habit_name,
            "category": category,
            "start_date": str(datetime.date.today()),
            "completed": []
        }
        habits.append(habit)
        habit_listbox.insert(tk.END, f"{habit_name} ({category})")
        save_habits()
        messagebox.showinfo("Éxito", f"Hábito '{habit_name}' agregado en la categoría '{category}'.")
    else:
        messagebox.showerror("Error", "El campo de nombre está vacío.")
    habit_entry.delete(0, tk.END)

# Función para marcar un hábito como completado hoy
def mark_completed():
    selected_habit_index = habit_listbox.curselection()
    if selected_habit_index:
        habit_index = selected_habit_index[0]
        habit = habits[habit_index]
        today = str(datetime.date.today())
        
        if today not in habit["completed"]:
            habit["completed"].append(today)
            save_habits()
            messagebox.showinfo("Éxito", f"Hábito '{habit['name']}' marcado como completado hoy ({today}).")
        else:
            messagebox.showwarning("Advertencia", f"Ya marcaste el hábito '{habit['name']}' como completado hoy.")
    else:
        messagebox.showerror("Error", "Por favor, selecciona un hábito.")

# Función para mostrar los hábitos actuales y su progreso
def show_habits():
    if habits:
        habit_text = "\n".join([f"{habit['name']} - Categoría: {habit['category']} - Completado: {len(habit['completed'])} días" for habit in habits])
        messagebox.showinfo("Hábitos Actuales", habit_text)
    else:
        messagebox.showinfo("Hábitos Actuales", "No hay hábitos registrados.")

# Función para modificar el nombre y la categoría de un hábito
def modify_habit():
    selected_habit_index = habit_listbox.curselection()
    if selected_habit_index:
        habit_index = selected_habit_index[0]
        current_habit = habits[habit_index]

        # Crear un pop-up para editar el hábito
        modify_window = tk.Toplevel(root)
        modify_window.title("Modificar Hábito")

        tk.Label(modify_window, text="Nombre del hábito:").pack(pady=5)
        new_habit_entry = tk.Entry(modify_window)
        new_habit_entry.insert(0, current_habit["name"])
        new_habit_entry.pack(pady=5)

        tk.Label(modify_window, text="Categoría del hábito:").pack(pady=5)
        new_category_var = tk.StringVar(value=current_habit["category"])
        category_menu = tk.OptionMenu(modify_window, new_category_var, *categories)
        category_menu.pack(pady=5)

        def save_changes():
            new_name = new_habit_entry.get()
            new_category = new_category_var.get()
            if new_name:
                # Actualizar el hábito
                habits[habit_index]["name"] = new_name
                habits[habit_index]["category"] = new_category
                habit_listbox.delete(habit_index)
                habit_listbox.insert(habit_index, f"{new_name} ({new_category})")
                save_habits()
                messagebox.showinfo("Éxito", "Los cambios han sido guardados.")
                modify_window.destroy()
            else:
                messagebox.showerror("Error", "El campo de nombre no puede estar vacío.")

        tk.Button(modify_window, text="Guardar Cambios", command=save_changes).pack(pady=10)
        tk.Button(modify_window, text="Cancelar", command=modify_window.destroy).pack(pady=5)
    else:
        messagebox.showerror("Error", "Por favor selecciona un hábito para modificar.")

# Función para eliminar un hábito
def delete_habit():
    selected_habit_index = habit_listbox.curselection()
    if selected_habit_index:
        habit_index = selected_habit_index[0]
        habit_listbox.delete(habit_index)
        del habits[habit_index]
        save_habits()
        messagebox.showinfo("Éxito", "El hábito ha sido eliminado.")
    else:
        messagebox.showerror("Error", "Por favor selecciona un hábito para eliminar.")

# Función para mostrar las estadísticas de los hábitos
def show_statistics():
    if not habits:
        messagebox.showinfo("Estadísticas", "No hay hábitos registrados.")
        return

    habit_names = [habit["name"] for habit in habits]
    completed_days = [len(habit["completed"]) for habit in habits]

    plt.bar(habit_names, completed_days, color='skyblue')
    plt.xlabel('Hábitos')
    plt.ylabel('Días completados')
    plt.title('Estadísticas de seguimiento de hábitos')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Función para mostrar tendencias de hábitos
def show_trend(habit_index):
    habit = habits[habit_index]
    completed_dates = habit["completed"]

    # Convertir las fechas a objetos datetime y contar los días completados por fecha
    dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in completed_dates]
    days_count = {date: dates.count(date) for date in set(dates)}
    sorted_days = sorted(days_count.items())

    # Extraer fechas y conteos para graficar
    dates_sorted, counts_sorted = zip(*sorted_days)

    plt.plot(dates_sorted, counts_sorted, marker='o')
    plt.xlabel('Fecha')
    plt.ylabel('Días completados')
    plt.title(f'Tendencia del hábito: {habit["name"]}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Nueva función para seleccionar un hábito de una lista
def select_habit(callback):
    selection_window = tk.Toplevel(root)
    selection_window.title("Seleccionar Hábito")

    habit_listbox = tk.Listbox(selection_window)
    for habit in habits:
        habit_listbox.insert(tk.END, f"{habit['name']} ({habit['category']})")
    habit_listbox.pack(pady=10)

    def on_select():
        selected_index = habit_listbox.curselection()
        if selected_index:
            callback(selected_index[0])
            selection_window.destroy()
        else:
            messagebox.showerror("Error", "Por favor selecciona un hábito.")

    tk.Button(selection_window, text="Seleccionar", command=on_select).pack(pady=5)
    tk.Button(selection_window, text="Cancelar", command=selection_window.destroy).pack(pady=5)

# Función para mostrar tendencias
def show_trends():
    if not habits:
        messagebox.showinfo("Tendencias", "No hay hábitos registrados.")
        return

    select_habit(lambda index: show_trend(index))

# Cargar hábitos al iniciar la app
habits = load_habits()
categories = load_categories()



import tkinter as tk
from PIL import Image, ImageTk  # Para manejar imágenes con PIL
import requests

# Configuración de la ventana principal
root = tk.Tk()
root.title("Seguimiento de Hábitos")
root.geometry("900x600")  # Ajustar tamaño según necesidad

# Cargar imagen de fondo y ajustarla al tamaño de la ventana
image = Image.open("fondo.png")  # Cambia por la ruta de tu imagen
image = image.resize((1100, 800), Image.Resampling.LANCZOS)  # Redimensionar imagen a 900x600 (mismo tamaño que la ventana)
bg_image = ImageTk.PhotoImage(image)

# Crear un label para contener la imagen de fondo
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Expande la imagen al tamaño de la ventana


'''
# Obtener cita motivacional de la API
category = 'happiness'
api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
response = requests.get(api_url, headers={'X-Api-Key': 'UfzmMDWqiU962nYZGZurIw==nLlSvls0UwwXfycs'})
if response.status_code == requests.codes.ok:
    quotes = response.json()
    if quotes:
        motivationalquote = quotes[0]['quote']
    else:
        motivationalquote = "No se encontraron citas motivacionales."
else:
    motivationalquote = "Error al obtener la cita motivacional."
'''
# Configurar el layout de la ventana principal con grid
root.grid_rowconfigure(1, weight=1)  # Fila del contenido principal
root.grid_columnconfigure(0, weight=1)  # Columna izquierda (hábito y lista)
root.grid_columnconfigure(1, weight=1)  # Columna derecha (botones)

# Crear un frame con margen de color, centrado en la ventana (para la cita motivacional)
welcome_frame = tk.Frame(root, bg="#d494b2", padx=10, pady=10)  # Margen de color rojo
welcome_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")  # Ocupa ambas columnas, centrado

# Crear la etiqueta dentro del frame para la cita motivacional
welcome_label = tk.Label(welcome_frame, text="motivationalquote", font=("Segoe Script", 14), wraplength=500, bg="#f0f8ff")
welcome_label.pack()

# Sección izquierda (entrada de hábitos, lista)
# Etiqueta y entrada para agregar hábitos
habit_label = tk.Label(root, text="Nombre del hábito:", font=("Berlin Sans FB Demi", 12), bg="#deaf99", fg= "white")
habit_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

habit_entry = tk.Entry(root)
habit_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

# Menú desplegable para seleccionar la categoría
category_label = tk.Label(root, text="Categoría del hábito:", font=("Berlin Sans FB Demi", 12), bg="#deaf99", fg= "white")
category_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

category_var = tk.StringVar(value=categories[0])
category_menu = tk.OptionMenu(root, category_var, *categories)
category_menu.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

# Listbox para mostrar los hábitos agregados
habit_listbox = tk.Listbox(root)
habit_listbox.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")  # Expansible

# Cargar los hábitos en la lista al iniciar
for habit in habits:
    habit_listbox.insert(tk.END, f"{habit['name']} ({habit['category']})")

# Sección derecha (botones)
button_style = {"font": ("Berlin Sans FB Demi", 12), "bg": "#b594d4", "fg": "white", "activebackground": "#45a049", "width": 20}

buttons = [
    ("Agregar Hábito", add_habit),
    ("Marcar Completado", mark_completed),
    ("Modificar Hábito", modify_habit),
    ("Eliminar Hábito", delete_habit),
    ("Mostrar Hábitos", show_habits),
    ("Mostrar Estadísticas", show_statistics),
    ("Mostrar Tendencias", show_trends),
    ("Editar Categorías", edit_categories),
]

# Posicionar los botones en la columna derecha
row_index = 1
for btn_text, btn_command in buttons:
    button = tk.Button(root, text=btn_text, command=btn_command, **button_style)
    button.grid(row=row_index, column=1, padx=20, pady=5, sticky="ew")  # Expandirse en la columna
    row_index += 1

# Ejecutar la ventana principal
root.mainloop()