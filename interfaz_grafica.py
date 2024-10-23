import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import psycopg2

# Configuración de la conexión a la base de datos
DB_HOST = "localhost"
DB_NAME = "dbjuan"
DB_USER = "admin"
DB_PASS = "admin"

# Conexión a la base de datos (sin uso en este momento)
def connect_db():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

# Lista de empleados y doctores (por ahora no conectada a la base de datos)
empleados = []
doctores = []

# Función para volver al inicio de sesión
def logout():
    ventana_principal.destroy()
    login()

# Función para mostrar la pantalla de empleados
def pagina_empleados():
    ventana_empleados = tk.Toplevel()
    ventana_empleados.title("Empleados")

    # Icono de la aplicacion
    img = Image.open("icon.png")
    bg_img = ImageTk.PhotoImage(img)
    ventana_empleados.iconphoto(False, bg_img)
    
    # Crear tabla de empleados
    tree = ttk.Treeview(ventana_empleados, columns=("ID", "Nombre", "Apellido", "NSS", "Fecha_Nac", 
                                                    "Direccion", "Ciudad", "Sexo", "Salario", 
                                                    "NSS_sup", "N_dep"), show='headings')
    
    # Definir las cabeceras
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Apellido", text="Apellido")
    tree.heading("NSS", text="NSS")
    tree.heading("Fecha_Nac", text="Fecha de Nacimiento")
    tree.heading("Direccion", text="Dirección")
    tree.heading("Ciudad", text="Ciudad")
    tree.heading("Sexo", text="Sexo")
    tree.heading("Salario", text="Salario")
    tree.heading("NSS_sup", text="NSS del Supervisor")
    tree.heading("N_dep", text="Nº de Departamento")
    tree.pack(pady=10)

    # Función para actualizar la tabla de empleados
    def actualizar_tabla():
        for row in tree.get_children():
            tree.delete(row)
        for empleado in empleados:
            tree.insert("", tk.END, values=(empleado["ID"], empleado["Nombre"], empleado["Apellido"],
                                             empleado["NSS"], empleado["Fecha_Nac"], empleado["Direccion"],
                                             empleado["Ciudad"], empleado["Sexo"], empleado["Salario"],
                                             empleado["NSS_sup"], empleado["N_dep"]))

    # Inicializar la tabla de empleados
    actualizar_tabla()

# Función para mostrar la pantalla de doctores
def pagina_doctores():
    ventana_doctores = tk.Toplevel()
    ventana_doctores.title("Doctores")

    # Icono de la aplicacion
    img = Image.open("icon.png")
    bg_img = ImageTk.PhotoImage(img)
    ventana_doctores.iconphoto(False, bg_img)
    
    # Crear tabla de doctores
    tree = ttk.Treeview(ventana_doctores, columns=("ID", "Nombre", "Especialidad", "Teléfono", "Horario"), show='headings')
    
    # Definir las cabeceras
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Especialidad", text="Especialidad")
    tree.heading("Teléfono", text="Teléfono")
    tree.heading("Horario", text="Horario")
    tree.pack(pady=10)
    
    # Función para actualizar la tabla de doctores
    def actualizar_tabla():
        for row in tree.get_children():
            tree.delete(row)
        for doctor in doctores:
            tree.insert("", tk.END, values=(doctor["ID"], doctor["Nombre"], doctor["Especialidad"],
                                             doctor["Teléfono"], doctor["Horario"]))
    
    # Inicializar la tabla de doctores
    actualizar_tabla()

# Función para crear la ventana de inicio
def pantalla_inicio():
    global ventana_principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Pantalla de Inicio")
    
    # Cargar imagen de fondo
    try:
        img = Image.open("icon.png")
    except FileNotFoundError:
        print("Archivo de imagen no encontrado.")

    img = img.resize((400, 200), Image.Resampling.LANCZOS)
    bg_img = ImageTk.PhotoImage(img)
    
# Icono de la aplicacion
    ventana_principal.iconphoto(False, bg_img)


    # Mostrar imagen
    label_img = tk.Label(ventana_principal, image=bg_img)
    label_img.image = bg_img  # Mantener referencia de la imagen
    label_img.pack(pady=10)

    # Menú de navegación
    btn_inicio = tk.Button(ventana_principal, text="Inicio", state=tk.DISABLED)  # Ya estás en inicio
    btn_inicio.pack(pady=5)
    
    btn_empleados = tk.Button(ventana_principal, text="Empleados", command=pagina_empleados)
    btn_empleados.pack(pady=5)

    btn_doctores = tk.Button(ventana_principal, text="Doctores", command=pagina_doctores)
    btn_doctores.pack(pady=5)

    btn_logout = tk.Button(ventana_principal, text="Cerrar Sesión", command=logout)
    btn_logout.pack(pady=20)

    ventana_principal.mainloop()

# Función para el inicio de sesión
def login():
    global ventana_login
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")

    tk.Label(ventana_login, text="Usuario:").pack(pady=5)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack(pady=5)

    tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
    entry_contraseña = tk.Entry(ventana_login, show="*")
    entry_contraseña.pack(pady=5)
    # Icono de la aplicacion
    img = Image.open("icon.png")
    bg_img = ImageTk.PhotoImage(img)
    ventana_login.iconphoto(False, bg_img)


    def verificar_login():
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()

        if usuario == "admin" and contraseña == "1234":
            ventana_login.destroy()
            pantalla_inicio()  # Muestra la pantalla principal tras iniciar sesión
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    btn_login = tk.Button(ventana_login, text="Iniciar Sesión", command=verificar_login)
    btn_login.pack(pady=20)

    ventana_login.mainloop()

# Iniciar la aplicación con la pantalla de inicio de sesión
login()
