import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
import datetime
import os
import matplotlib.pyplot as plt



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



# Configuración de la ventana principal
root = tk.Tk()
root.title("Seguimiento de Hábitos")


import requests

category = 'happiness'
api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
response = requests.get(api_url, headers={'X-Api-Key': 'UfzmMDWqiU962nYZGZurIw==nLlSvls0UwwXfycs'})
if response.status_code == requests.codes.ok:
    quotes = response.json()  # Convierte la respuesta JSON en un objeto Python
    if quotes:  # Verifica que la lista de citas no esté vacía
        motivationalquote = quotes[0]['quote']  # Accede a la primera cita
        print(motivationalquote)  # Imprime solo la cita
    else:
        print("No se encontraron citas.")
else:
    print("Error:", response.status_code, response.text)

# Agregar el mensaje de bienvenida
welcome_label = tk.Label(root, text= motivationalquote, font=("Arial", 14))
welcome_label.pack(pady=10)  # Ajusta el padding según sea necesario

# Lista de categorías predefinidas
categories = ["Salud", "Trabajo", "Ocio", "Personal", "Estudio"]
category_var = tk.StringVar(value=categories[0])  # Valor por defecto

# Etiqueta y entrada para agregar hábitos
tk.Label(root, text="Nombre del hábito:").pack(pady=10)
habit_entry = tk.Entry(root)
habit_entry.pack()

# Menú desplegable para seleccionar la categoría
tk.Label(root, text="Categoría del hábito:").pack(pady=10)
category_menu = tk.OptionMenu(root, category_var, *categories)
category_menu.pack()

# Listbox para mostrar los hábitos agregados
habit_listbox = tk.Listbox(root)
habit_listbox.pack(pady=10)


# Cargar los hábitos en la lista al iniciar
for habit in habits:
    habit_listbox.insert(tk.END, f"{habit['name']} ({habit['category']})")

# Botones para agregar, marcar completado, modificar y eliminar hábitos
tk.Button(root, text="Agregar Hábito", command=add_habit).pack(pady=5)
tk.Button(root, text="Marcar Completado", command=mark_completed).pack(pady=5)
tk.Button(root, text="Modificar Hábito", command=modify_habit).pack(pady=5)
tk.Button(root, text="Eliminar Hábito", command=delete_habit).pack(pady=5)
tk.Button(root, text="Mostrar Hábitos", command=show_habits).pack(pady=5)
tk.Button(root, text="Mostrar Estadísticas", command=show_statistics).pack(pady=5)
tk.Button(root, text="Mostrar Tendencias", command=show_trends).pack(pady=5)

root.mainloop()
