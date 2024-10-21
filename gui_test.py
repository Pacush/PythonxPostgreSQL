import tkinter as tk
from tkinter import messagebox

# Función para centrar y redimensionar ventanas
def centrar_ventana(ventana):
    # Obtener el tamaño de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    # Calcular la mitad del tamaño de la pantalla
    ancho_ventana = ancho_pantalla // 2
    alto_ventana = alto_pantalla // 2
    
    # Calcular la posición para centrar la ventana
    x_pos = (ancho_pantalla - ancho_ventana) // 2
    y_pos = (alto_pantalla - alto_ventana) // 2
    
    # Configurar el tamaño y la posición de la ventana
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Ventana de login
def login():
    def check_login():
        user = entry_user.get()
        password = entry_pass.get()

        if user == "admin" and password == "1234":  # Contraseña actualizada
            ventana_login.destroy()  # Cierra la ventana de login
            abrir_menu_principal()  # Abre el menú principal
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    
    frame_login = tk.Frame(ventana_login)
    frame_login.pack(expand=True, fill="both")
    
    label_user = tk.Label(frame_login, text="Usuario:")
    label_user.pack(pady=5)
    
    entry_user = tk.Entry(frame_login)
    entry_user.pack(pady=5)
    
    label_pass = tk.Label(frame_login, text="Contraseña:")
    label_pass.pack(pady=5)
    
    entry_pass = tk.Entry(frame_login, show="*")
    entry_pass.pack(pady=5)
    
    btn_login = tk.Button(frame_login, text="Login", command=check_login)
    btn_login.pack(pady=10)
    
    # Centrar y redimensionar la ventana de login
    centrar_ventana(ventana_login)
    
    ventana_login.mainloop()

# Ventana principal (menú)
def abrir_menu_principal():
    ventana_menu = tk.Tk()
    ventana_menu.title("Gestor de registros")
    
    # Crear un frame para centrar todo el contenido
    frame_centrado = tk.Frame(ventana_menu)
    frame_centrado.pack(expand=True)

    # Usar un grid layout dentro de frame_centrado
    frame_menu = tk.Frame(frame_centrado)
    frame_menu.grid(row=0, column=0, padx=20, pady=20)  # Grid centrado en la ventana
    
    # Título en la parte superior
    label_title = tk.Label(frame_menu, text="Gestor de registros", font=("Arial", 24))
    label_title.grid(row=0, column=0, columnspan=2, pady=20)
    
    # Crear botones alineados a la izquierda
    btn1 = tk.Button(frame_menu, text="Botón 1", command=abrir_ventana_boton1, width=20)
    btn1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    btn2 = tk.Button(frame_menu, text="Botón 2", command=abrir_ventana_boton2, width=20)
    btn2.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    
    btn3 = tk.Button(frame_menu, text="Botón 3", command=abrir_ventana_boton3, width=20)
    btn3.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    
    # Imagen alineada a la derecha
    logo_img = tk.PhotoImage(file="logo.png")  # Usar la ruta "logo.png"
    label_logo = tk.Label(frame_menu, image=logo_img)
    label_logo.grid(row=1, column=1, rowspan=3, padx=20, pady=10, sticky="e")
    
    # Centrar y redimensionar la ventana de menú
    centrar_ventana(ventana_menu)
    
    ventana_menu.mainloop()

# Ventanas de cada botón
def abrir_ventana_boton1():
    ventana = tk.Toplevel()
    ventana.title("Ventana Botón 1")
    
    frame_boton1 = tk.Frame(ventana)
    frame_boton1.pack(expand=True, fill="both")
    
    label = tk.Label(frame_boton1, text="Esta es la ventana del Botón 1")
    label.pack(pady=20)
    
    # Centrar y redimensionar la ventana
    centrar_ventana(ventana)

def abrir_ventana_boton2():
    ventana = tk.Toplevel()
    ventana.title("Ventana Botón 2")
    
    frame_boton2 = tk.Frame(ventana)
    frame_boton2.pack(expand=True, fill="both")
    
    label = tk.Label(frame_boton2, text="Esta es la ventana del Botón 2")
    label.pack(pady=20)
    
    # Centrar y redimensionar la ventana
    centrar_ventana(ventana)

def abrir_ventana_boton3():
    ventana = tk.Toplevel()
    ventana.title("Ventana Botón 3")
    
    frame_boton3 = tk.Frame(ventana)
    frame_boton3.pack(expand=True, fill="both")
    
    label = tk.Label(frame_boton3, text="Esta es la ventana del Botón 3")
    label.pack(pady=20)
    
    # Centrar y redimensionar la ventana
    centrar_ventana(ventana)

# Iniciar el programa con la ventana de login
login()
