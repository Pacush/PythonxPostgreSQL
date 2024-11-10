import tkinter as tk
from datetime import datetime
from tkinter import ttk

from tkcalendar import Calendar


def obtener_cita():
    # Obtener la fecha seleccionada en el calendario
    selected_date = cal.selection_get()

    # Obtener la hora seleccionada (en formato 1, 2, 3, etc.) y agregar ":00" para mostrar la hora completa
    time = hour_combobox.get()
    time = time[0]
    
    selected_time = f"{time}:00"

    # Combinar la fecha y hora seleccionadas
    appointment = f"Cita agendada para: {selected_date} a las {selected_time}"

    # Mostrar la cita agendada
    appointment_label.config(text=appointment)



def abrir_ventana_calenario_citas():
    # Crear la ventana principal
    ventana_calendario = tk.Tk()
    ventana_calendario.title('Registrar cita')

    # Calendario
    global cal
    cal = Calendar(ventana_calendario, selectmode='day', year=2024, month=11, day=20)
    cal.pack(pady=20)

    # Reloj (hora)
    hour_label = tk.Label(ventana_calendario, text="Hora:")
    hour_label.pack(pady=5)

    # Combobox para seleccionar la hora (en formato 1:00, 2:00, ..., 12:00)
    global hour_combobox
    hour_combobox = ttk.Combobox(ventana_calendario, values=[f"{i}:00 - {i + 1}:00" for i in range(9, 20)], width=12)
    hour_combobox.set("9:00 - 10:00")  # valor por defecto
    hour_combobox.pack(pady=20)

    # Botón para agendar cita
    tk.Button(ventana_calendario, text='Agendar Cita', command=obtener_cita).pack(pady=20)

    # Etiqueta para mostrar la cita agendada
    global appointment_label
    appointment_label = tk.Label(ventana_calendario, text="", font=("Helvetica", 12))
    appointment_label.pack(pady=20)
    
    ventana_calendario.mainloop()




#ventana_calendario.mainloop()
abrir_ventana_calenario_citas()
