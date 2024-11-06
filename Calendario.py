import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

def print_appointment():
    # Obtener la fecha seleccionada en el calendario
    selected_date = cal.selection_get()

    # Obtener la hora seleccionada (en formato 1, 2, 3, etc.) y agregar ":00" para mostrar la hora completa
    selected_time = f"{hour_combobox.get()}:00"

    # Combinar la fecha y hora seleccionadas
    appointment = f"Cita agendada para: {selected_date} a las {selected_time}"

    # Mostrar la cita agendada
    appointment_label.config(text=appointment)

# Crear la ventana principal
root = tk.Tk()
root.title('Calendario interactivo con Reloj')

# Calendario
cal = Calendar(root, selectmode='day', year=2024, month=11, day=20)
cal.pack(pady=20)

# Reloj (hora)
hour_label = tk.Label(root, text="Hora:")
hour_label.pack(pady=5)

# Combobox para seleccionar la hora (en formato 1:00, 2:00, ..., 12:00)
hour_combobox = ttk.Combobox(root, values=[f"{i}:00" for i in range(9, 20)], width=5)
hour_combobox.set("9:00")  # valor por defecto
hour_combobox.pack(pady=5)

# Botón para agendar cita
tk.Button(root, text='Agendar Cita', command=print_appointment).pack(pady=20)

# Etiqueta para mostrar la cita agendada
appointment_label = tk.Label(root, text="", font=("Helvetica", 12))
appointment_label.pack(pady=20)

root.mainloop()
