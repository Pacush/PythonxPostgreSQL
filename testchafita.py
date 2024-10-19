import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2

# Intentar la conexión a la base de datos
try:
    connection = psycopg2.connect(
        host='localhost',
        user='admin',
        password='admin',
        database='dbjuan',
        port='5433'
    )
    cursor = connection.cursor()
    print('Conexión exitosa')

except Exception as ex:
    print("Error al conectar a la base de datos:", ex)

default_user = "admin"
default_password = "1234"

# Función para mostrar la nueva ventana con la tabla
def open_new_window():
    ventana = tk.Toplevel()  # Crear una nueva ventana secundaria
    ventana.title("Ventana Principal")

    # Configurar el logo de la nueva ventana
    try:
        logo = tk.PhotoImage(file="icon.png")
        ventana.iconphoto(False, logo)
    except Exception as e:
        print("No se pudo cargar el icono:", e)

    # Centramos la nueva ventana en la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    new_window_width = screen_width // 3
    new_window_height = screen_height // 3
    x = (screen_width // 2) - (new_window_width // 2)
    y = (screen_height // 2) - (new_window_height // 2)
    ventana.geometry(f"{new_window_width}x{new_window_height}+{x}+{y}")

    # Crear un marco para la tabla y las barras de desplazamiento
    frame = tk.Frame(ventana)
    frame.pack(fill="both", expand=True)

    # Crear la tabla con el Treeview y agregar las barras de desplazamiento
    tabla = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10), show="headings", height=10)
    
    # Configurar los encabezados de la tabla
    tabla.heading(1, text="Nombre")
    tabla.heading(2, text="Apellido")
    tabla.heading(3, text="NSS")
    tabla.heading(4, text="Fecha Nacimiento")
    tabla.heading(5, text="Direccion")
    tabla.heading(6, text="Ciudad")
    tabla.heading(7, text="Sexo")
    tabla.heading(8, text="Salario")
    tabla.heading(9, text="NSS Sup")
    tabla.heading(10, text="Num. Dpto.")

    # Ajustar las columnas
    for col in range(0, 10):
        tabla.column(col, anchor='center', width=100)

    # Crear la barra de desplazamiento vertical
    scrollbar_vertical = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar_vertical.set)

    # Crear la barra de desplazamiento horizontal
    scrollbar_horizontal = ttk.Scrollbar(frame, orient="horizontal", command=tabla.xview)
    tabla.configure(xscroll=scrollbar_horizontal.set)

    # Posicionar la tabla y los scrollbars
    tabla.grid(row=0, column=0, sticky="nsew")
    scrollbar_vertical.grid(row=0, column=1, sticky="ns")
    scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

    # Expandir la tabla y los scrollbars para llenar el espacio del marco
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Ejecutar la consulta SQL y rellenar la tabla
    try:
        cursor.execute("SELECT * FROM compania.empleado")
        rows = cursor.fetchall()
        for row in rows:
            tabla.insert('', 'end', values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar la consulta: {e}")

    ventana.mainloop()

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
login_window_width = screen_width // 5
login_window_height = screen_height // 5
x = (screen_width // 2) - (login_window_width // 2)
y = (screen_height // 2) - (login_window_height // 2)

root.geometry(f"{login_window_width}x{login_window_height}+{x}+{y}")
root.title("Inicio de Sesión")

# Configurar el logo de la ventana principal
try:
    logo = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, logo)
except Exception as e:
    print("No se pudo cargar el icono:", e)

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

# Cerrar la conexión a la base de datos al final
if connection:
    cursor.close()
    connection.close()
    print("Conexión cerrada.")
