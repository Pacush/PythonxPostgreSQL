import tkinter as tk
from tkinter import messagebox
import psycopg2

try:
    connection=psycopg2.connect(
        host='localhost',
        user='admin',
        password='admin',
        database='dbjuan',
        port='5433'
    )

    print('Conexión exitosa')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM compania.empleado")
    rows=cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)

default_user = "admin"
default_password = "1234"

# Función para mostrar la nueva ventana con botones
def open_new_window():
    new_root = tk.Tk()  # Crear una nueva ventana principal
    new_root.title("Ventana Principal")
    
    # Centramos la nueva ventana en la pantalla
    screen_width = new_root.winfo_screenwidth()
    screen_height = new_root.winfo_screenheight()
    new_window_width = screen_width // 3
    new_window_height = screen_height // 3
    x = (screen_width // 2) - (new_window_width // 2)
    y = (screen_height // 2) - (new_window_height // 2)
    
    new_root.geometry(f"{new_window_width}x{new_window_height}+{x}+{y}")
    
    # Configurar el logo de la nueva ventana
    logo = tk.PhotoImage(file="icon.png")
    new_root.iconphoto(False, logo)

    # Crear botones apilados en el centro
    button1 = tk.Button(new_root, text="Botón 1")
    button2 = tk.Button(new_root, text="Botón 2")
    button3 = tk.Button(new_root, text="Botón 3")
    
    button1.pack(pady=10, expand=True)
    button2.pack(pady=10, expand=True)
    button3.pack(pady=10, expand=True)
    
    new_root.mainloop()  # Mantener la nueva ventana activa

# Función para validar las credenciales
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == default_user and password == default_password:
        messagebox.showinfo("Inicio de sesión", "¡Inicio de sesión exitoso!")
        root.destroy()  # Cerrar la ventana de login
        open_new_window()  # Abrir la nueva ventana
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

# Crear la ventana principal (de login)
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
login_window_width = screen_width / 5
login_window_height = screen_height / 5
x = (screen_width // 2) - (login_window_width // 2)
y = (screen_height // 2) - (login_window_height // 2)

window_height = int(login_window_height)
window_width = int(login_window_width)
x = int(x)
y = int(y)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Cambia "400x300" al tamaño que desees
root.title("Inicio de Sesión")

# Configurar el logo de la ventana principal
logo = tk.PhotoImage(file="icon.png")  # Asegúrate de cambiar la ruta
root.iconphoto(False, logo)

# Crear etiquetas y entradas para el usuario y la contraseña
label_username = tk.Label(root, text="Usuario:")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Contraseña:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Crear un botón de inicio de sesión
button_login = tk.Button(root, text="Inicio de sesión", command=login)
button_login.pack(pady=20)

# Iniciar el bucle de la interfaz gráfica
root.mainloop()
