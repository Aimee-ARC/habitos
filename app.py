import tkinter as tk
from tkinter import messagebox
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
    if habit_name:
        habit = {
            "name": habit_name,
            "start_date": str(datetime.date.today()),
            "completed": []
        }
        habits.append(habit)
        habit_listbox.insert(tk.END, habit_name)
        save_habits()
        messagebox.showinfo("Éxito", f"Hábito '{habit_name}' agregado.")
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
        habit_text = "\n".join([f"{habit['name']} - Completado: {len(habit['completed'])} días" for habit in habits])
        messagebox.showinfo("Hábitos Actuales", habit_text)
    else:
        messagebox.showinfo("Hábitos Actuales", "No hay hábitos registrados.")

# Función para modificar el nombre de un hábito
def modify_habit():
    selected_habit_index = habit_listbox.curselection()
    new_name = habit_entry.get()
    if selected_habit_index and new_name:
        habit_index = selected_habit_index[0]
        habits[habit_index]["name"] = new_name
        habit_listbox.delete(habit_index)
        habit_listbox.insert(habit_index, new_name)
        save_habits()
        messagebox.showinfo("Éxito", f"El hábito fue renombrado a '{new_name}'.")
    else:
        messagebox.showerror("Error", "Por favor selecciona un hábito y escribe el nuevo nombre.")

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

# Cargar hábitos al iniciar la app
habits = load_habits()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Seguimiento de Hábitos")

# Etiqueta y entrada para agregar, modificar o eliminar hábitos
tk.Label(root, text="Nombre del hábito:").pack(pady=10)
habit_entry = tk.Entry(root)
habit_entry.pack()

# Listbox para mostrar los hábitos agregados
habit_listbox = tk.Listbox(root)
habit_listbox.pack(pady=10)

# Cargar los hábitos en la lista al iniciar
for habit in habits:
    habit_listbox.insert(tk.END, habit["name"])

# Botones para agregar, marcar completado, modificar y eliminar hábitos
tk.Button(root, text="Agregar Hábito", command=add_habit).pack(pady=5)
tk.Button(root, text="Marcar Completado", command=mark_completed).pack(pady=5)
tk.Button(root, text="Modificar Hábito", command=modify_habit).pack(pady=5)
tk.Button(root, text="Eliminar Hábito", command=delete_habit).pack(pady=5)
tk.Button(root, text="Ver Hábitos", command=show_habits).pack(pady=5)

# Botón para mostrar estadísticas
tk.Button(root, text="Mostrar Estadísticas", command=show_statistics).pack(pady=5)

root.mainloop()
