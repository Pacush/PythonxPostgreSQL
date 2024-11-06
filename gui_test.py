import tkinter as tk
from tkinter import messagebox, ttk

import psycopg2
from PIL import Image, ImageTk


# Conexión a la base de datos
def conectar_db():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='12345',
            database='NucleoDeDiagnostico',
            port='5432'
        )
        cursor = connection.cursor()
        return connection, cursor
    except Exception as ex:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {ex}")
        return None, None

# Función para centrar y redimensionar ventanas
def centrar_ventana(ventana, ancho_ventana_ratio, alto_ventana_ratio, pos_offset):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    ancho_ventana = ancho_pantalla // ancho_ventana_ratio
    alto_ventana = alto_pantalla // alto_ventana_ratio
    x_pos = (ancho_pantalla - ancho_ventana) // pos_offset
    y_pos = (alto_pantalla - alto_ventana) // pos_offset
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

def cargar_logo(ventana):
    try:
        logo = tk.PhotoImage(file="icon.png")
        ventana.iconphoto(False, logo)
    except Exception as e:
        print("No se pudo cargar el icono:", e)

def refresh_table(treeview, tabla):
    # Borrar los datos actuales en el treeview
    for item in treeview.get_children():
        treeview.delete(item)
    
    # Re-cargar datos desde la base de datos
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute(f"SELECT * FROM {tabla} ORDER BY codigo ASC")
        rows = cursor.fetchall()
        for row in rows:
            treeview.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
        
    else:
        print("Fallo")

# Ventana de login
def login():
    def check_login():
        user = entry_user.get()
        password = entry_pass.get()

        connection, cursor = conectar_db()
        
        if connection and cursor:
            if user == "admin" and password == "1234":
                ventana_login.destroy()
                abrir_menu_principal()
        
            else:
                #Conuslta verificar empleado
                cursor.execute("SELECT * FROM empleados where codigo =%s AND contrasena = %s", (user, password))
                empleado = cursor.fetchone()

                if empleado:
                    ventana_login.destroy()
                    abrir_menu_principal()
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos")

            cursor.close()
            connection.close()

        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
    
    ventana_login = tk.Tk()
    ventana_login.title("Login")
    
    cargar_logo(ventana_login)

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
    
    centrar_ventana(ventana_login, 5, 3, 2)
    ventana_login.mainloop()

# Ventana principal (menú)
def abrir_menu_principal():
    global ventana_menu
    ventana_menu = tk.Tk()
    ventana_menu.title("Gestor de registros")
    cargar_logo(ventana_menu)
    
    frame_centrado = tk.Frame(ventana_menu)
    frame_centrado.pack(expand=True)

    frame_menu = tk.Frame(frame_centrado)
    frame_menu.grid(row=0, column=0, padx=20, pady=20)
    
    label_title = tk.Label(frame_menu, text="Gestor de registros", font=("Arial", 24))
    label_title.grid(row=0, column=0, columnspan=2, pady=20)
    
    btn1 = tk.Button(frame_menu, text="Empleados", command=abrir_ventana_empleados, width=20)
    btn1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    btn2 = tk.Button(frame_menu, text="Doctores", command=abrir_ventana_doctores , width=20)
    btn2.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    btn3 = tk.Button(frame_menu, text="Pacientes", command=abrir_ventana_pacientes, width=20)
    btn3.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    
    btn4 = tk.Button(frame_menu, text="Cerrar sesión", width=20, command=cerrar_sesion)
    btn4.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    
    logo_img = tk.PhotoImage(file="logo2.png")
    label_logo = tk.Label(frame_menu, image=logo_img)
    label_logo.grid(row=1, column=1, rowspan=3, padx=20, pady=10, sticky="e")
    
    centrar_ventana(ventana_menu, 2, 2, 2)
    ventana_menu.mainloop()

# Ventana de empleados
def abrir_ventana_empleados():
    global ventana_empleados
    ventana_empleados = tk.Toplevel()
    ventana_empleados.title("Empleados")
    cargar_logo(ventana_empleados)
    
    frame_principal = tk.Frame(ventana_empleados)
    frame_principal.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Crear tabla con scrollbars
    tree_frame = tk.Frame(frame_principal)
    tree_frame.pack(fill="both", expand=True)
    
    # Scrollbars
    scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")
    
    scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")
    
    # Definir columnas de la tabla empleados
    global tablaEmpleados
    tablaEmpleados = ttk.Treeview(tree_frame, columns=("codigo", "nombre", "direccion", "telefono", "fecha_nac", "sexo", "sueldo", "turno", "contrasena"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tablaEmpleados.pack(fill="both", expand=True)
    
    # Configuración de las columnas
    tablaEmpleados.heading("codigo", text="Código")
    tablaEmpleados.heading("nombre", text="Nombre")
    tablaEmpleados.heading("direccion", text="Dirección")
    tablaEmpleados.heading("telefono", text="Teléfono")
    tablaEmpleados.heading("fecha_nac", text="Fecha Nacimiento")
    tablaEmpleados.heading("sexo", text="Sexo")
    tablaEmpleados.heading("sueldo", text="Sueldo")
    tablaEmpleados.heading("turno", text="Turno")
    tablaEmpleados.heading("contrasena", text="Contraseña")
    
    # Ajustar el tamaño de las columnas
    tablaEmpleados.column("codigo", width=80)
    tablaEmpleados.column("nombre", width=150)
    tablaEmpleados.column("direccion", width=200)
    tablaEmpleados.column("telefono", width=100)
    tablaEmpleados.column("fecha_nac", width=120)
    tablaEmpleados.column("sexo", width=80)
    tablaEmpleados.column("sueldo", width=100)
    tablaEmpleados.column("turno", width=80)
    tablaEmpleados.column("contrasena", width=120)
    
    # Asignar los scrollbars al Treeview
    scrollbar_y.config(command=tablaEmpleados.yview)
    scrollbar_x.config(command=tablaEmpleados.xview)
    
    # Botones para registrar, editar y eliminar empleados
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Registrar", width=15, command=registrar_empleado)
    btn_registrar.pack(side="left", padx=10)
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15)
    btn_eliminar.pack(side="left", padx=10)
    
    refresh_image = Image.open("refresh.png")  # Carga la imagen
    refresh_image = refresh_image.resize((15, 15), Image.LANCZOS)  # Redimensiona según sea necesario
    refresh_icon = ImageTk.PhotoImage(refresh_image)  # Convierte para usar en tkinter
    
    btn_refresh = tk.Button(button_frame, text="Refresh", width=15, command=lambda: refresh_table(tablaEmpleados, "empleados"))
    btn_refresh.pack(side="right", padx=10)
    
    
    # Conectar y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM empleados ORDER BY codigo ASC")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tablaEmpleados.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_empleados, 2, 2, 3)

def registrar_empleado():
    # Ventana para registrar nuevo empleado
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registrar nuevo empleado")
    cargar_logo(ventana_registro)
    
    frame_registro = tk.Frame(ventana_registro)
    frame_registro.pack(padx=10, pady=10)

    # Campos para registrar empleado
    labels = ["Nombre", "Dirección", "Teléfono", "Fecha Nac (YYYY-MM-DD)", "Sexo", "Sueldo", "Turno", "Contraseña"]
    entries = []

    for label_text in labels:
        label = tk.Label(frame_registro, text=label_text)
        label.pack(pady=2)
        entry = tk.Entry(frame_registro)
        entry.pack(pady=2)
        entries.append(entry)

    def guardar_empleado():
        # Recuperar los valores de los campos
        valores = [entry.get() for entry in entries]
        if all(valores):
            try:
                connection, cursor = conectar_db()
                if connection and cursor:
                    query = """
                        INSERT INTO empleados (nombre, direccion, telefono, fecha_nac, sexo, sueldo, turno, contrasena)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, tuple(valores))
                    connection.commit()
                    messagebox.showinfo("Éxito", "Empleado registrado exitosamente")
                    cursor.close()
                    connection.close()
                    ventana_registro.destroy()  # Cerrar la ventana de registro después de guardar
                    ventana_empleados.lift()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                    ventana_registro.destroy()
                    ventana_empleados.lift()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el doctor: {e}")
                ventana_registro.lift()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            ventana_registro.lift()
    
    refresh_table(tablaEmpleados, "empleados")
    
    # Botón para guardar doctor
    btn_guardar = tk.Button(frame_registro, text="Guardar", command=guardar_empleado)
    btn_guardar.pack(pady=10, side="left")
    btn_cancelar = tk.Button(frame_registro, text="Cancelar", command=ventana_registro.destroy)
    btn_cancelar.pack(pady=10, side="right")
    
    centrar_ventana(ventana_registro, 4, 2, 3)

# Ventana de doctores
def abrir_ventana_doctores():
    global ventana_doctores
    ventana_doctores = tk.Toplevel()
    ventana_doctores.title("Doctores")
    cargar_logo(ventana_doctores)
    
    frame_principal = tk.Frame(ventana_doctores)
    frame_principal.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Crear tabla con scrollbars
    tree_frame = tk.Frame(frame_principal)
    tree_frame.pack(fill="both", expand=True)
    
    # Scrollbars
    scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")
    
    scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")
    
    # Definir columnas de la tabla doctores
    global tablaDoctores
    tablaDoctores = ttk.Treeview(tree_frame, columns=("codigo", "nombre", "direccion", "telefono", "fecha_nac", "sexo", "especialidad", "contrasena"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tablaDoctores.pack(fill="both", expand=True)
    
    # Configuración de las columnas
    tablaDoctores.heading("codigo", text="Código")
    tablaDoctores.heading("nombre", text="Nombre")
    tablaDoctores.heading("direccion", text="Dirección")
    tablaDoctores.heading("telefono", text="Teléfono")
    tablaDoctores.heading("fecha_nac", text="Fecha Nacimiento")
    tablaDoctores.heading("sexo", text="Sexo")
    tablaDoctores.heading("especialidad", text="Especialidad")
    tablaDoctores.heading("contrasena", text="Contraseña")
    
    # Ajustar el tamaño de las columnas
    tablaDoctores.column("codigo", width=80)
    tablaDoctores.column("nombre", width=150)
    tablaDoctores.column("direccion", width=200)
    tablaDoctores.column("telefono", width=100)
    tablaDoctores.column("fecha_nac", width=120)
    tablaDoctores.column("sexo", width=80)
    tablaDoctores.column("especialidad", width=80)
    tablaDoctores.column("contrasena", width=120)
    
    # Asignar los scrollbars al Treeview
    scrollbar_y.config(command=tablaDoctores.yview)
    scrollbar_x.config(command=tablaDoctores.xview)
    
    # Botones para registrar, editar y eliminar doctores
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Registrar", width=15, command=registrar_doctor)
    btn_registrar.pack(side="left", padx=10)
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15)
    btn_eliminar.pack(side="left", padx=10)
    
    btn_refresh = tk.Button(button_frame, text="Refresh", width=15, command=lambda: refresh_table(tablaDoctores, "doctores"))
    btn_refresh.pack(side="right", padx=10)
    
    # Conectar y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM doctores ORDER BY codigo ASC")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tablaDoctores.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_doctores, 2, 2, 3)

# Ventana para registrar un nuevo doctor, reutilizando la de empleados
def registrar_doctor():
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registrar nuevo doctor")
    cargar_logo(ventana_registro)
    
    frame_registro = tk.Frame(ventana_registro)
    frame_registro.pack(padx=10, pady=10)

    # Campos para registrar doctor
    labels = ["Nombre", "Dirección", "Teléfono", "Fecha Nac (YYYY-MM-DD)", "Sexo", "Especialidad", "Contraseña"]
    entries = []

    for label_text in labels:
        label = tk.Label(frame_registro, text=label_text)
        label.pack(pady=2)
        entry = tk.Entry(frame_registro)
        entry.pack(pady=2)
        entries.append(entry)

    def guardar_doctor():
        # Recuperar los valores de los campos
        valores = [entry.get() for entry in entries]
        if all(valores):
            try:
                connection, cursor = conectar_db()
                if connection and cursor:
                    query = """
                        INSERT INTO doctores (nombre, direccion, telefono, fecha_nac, sexo, especialidad, contrasena)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, tuple(valores))
                    connection.commit()
                    messagebox.showinfo("Éxito", "Doctor registrado exitosamente")
                    cursor.close()
                    connection.close()
                    ventana_registro.destroy()  # Cerrar la ventana de registro después de guardar
                    ventana_doctores.lift()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                    ventana_registro.destroy()
                    ventana_doctores.lift()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el doctor: {e}")
                ventana_registro.lift()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            ventana_registro.lift()
        
        refresh_table(tablaDoctores, "doctores")
        
    # Botón para guardar doctor
    btn_guardar = tk.Button(frame_registro, text="Guardar", command=guardar_doctor)
    btn_guardar.pack(pady=10, side="left")
    btn_cancelar = tk.Button(frame_registro, text="Cancelar", command=ventana_registro.destroy)
    btn_cancelar.pack(pady=10, side="right")

    centrar_ventana(ventana_registro, 4, 2, 3)

# Ventana de empleados
def abrir_ventana_pacientes():
    global ventana_pacientes
    ventana_pacientes= tk.Toplevel()
    ventana_pacientes.title("Pacientes")
    cargar_logo(ventana_pacientes)
    
    frame_principal = tk.Frame(ventana_pacientes)
    frame_principal.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Crear tabla con scrollbars
    tree_frame = tk.Frame(frame_principal)
    tree_frame.pack(fill="both", expand=True)
    
    # Scrollbars
    scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")
    
    scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")
    
    # Definir columnas de la tabla empleados
    global tablaPacientes
    tablaPacientes = ttk.Treeview(tree_frame, columns=("codigo", "nombre", "direccion", "telefono", "fecha_nac", "sexo", "edad", "estatura"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tablaPacientes.pack(fill="both", expand=True)
    
    # Configuración de las columnas
    tablaPacientes.heading("codigo", text="Código")
    tablaPacientes.heading("nombre", text="Nombre")
    tablaPacientes.heading("direccion", text="Dirección")
    tablaPacientes.heading("telefono", text="Teléfono")
    tablaPacientes.heading("fecha_nac", text="Fecha Nacimiento")
    tablaPacientes.heading("sexo", text="Sexo")
    tablaPacientes.heading("edad", text="Edad")
    tablaPacientes.heading("estatura", text="Estatura")
    
    # Ajustar el tamaño de las columnas
    tablaPacientes.column("codigo", width=80)
    tablaPacientes.column("nombre", width=150)
    tablaPacientes.column("direccion", width=200)
    tablaPacientes.column("telefono", width=100)
    tablaPacientes.column("fecha_nac", width=120)
    tablaPacientes.column("sexo", width=80)
    tablaPacientes.column("edad", width=80)
    tablaPacientes.column("estatura", width=80)
    
    # Asignar los scrollbars al Treeview
    scrollbar_y.config(command=tablaPacientes.yview)
    scrollbar_x.config(command=tablaPacientes.xview)
    
    # Botones para registrar, editar y eliminar empleados
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Registrar", width=15, command=registrar_paciente)
    btn_registrar.pack(side="left", padx=10)
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15)
    btn_eliminar.pack(side="left", padx=10)
    
    btn_refresh = tk.Button(button_frame, text="Refresh", width=15, command=lambda: refresh_table(tablaPacientes, "pacientes"))
    btn_refresh.pack(side="right", padx=10)
    
    # Conectar y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM pacientes ORDER BY codigo ASC")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tablaPacientes.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_pacientes, 2, 2, 3)

def registrar_paciente():
    # Ventana para registrar nuevo empleado
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registrar nuevo paciente")
    cargar_logo(ventana_registro)
    
    frame_registro = tk.Frame(ventana_registro)
    frame_registro.pack(padx=10, pady=10)

    # Campos para registrar empleado
    labels = ["Nombre", "Dirección", "Teléfono", "Fecha Nac (YYYY-MM-DD)", "Sexo", "Edad", "Estatura (metros)"]
    entries = []

    for label_text in labels:
        label = tk.Label(frame_registro, text=label_text)
        label.pack(pady=2)
        entry = tk.Entry(frame_registro)
        entry.pack(pady=2)
        entries.append(entry)

    def guardar_paciente():
        # Recuperar los valores de los campos
        valores = [entry.get() for entry in entries]
        if all(valores):
            try:
                connection, cursor = conectar_db()
                if connection and cursor:
                    query = """
                        INSERT INTO pacientes (nombre, direccion, telefono, fecha_nac, sexo, edad, estatura)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, tuple(valores))
                    connection.commit()
                    messagebox.showinfo("Éxito", "Paciente registrado exitosamente")
                    cursor.close()
                    connection.close()
                    ventana_registro.destroy()  # Cerrar la ventana de registro después de guardar
                    ventana_pacientes.lift()
                    
                    
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                    ventana_registro.destroy()
                    ventana_pacientes.lift()

                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar al paciente: {e}")
                ventana_registro.lift()
                
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            ventana_registro.lift()
            
        refresh_table(tablaPacientes, "pacientes")
    
    # Botón para guardar empleado
    btn_guardar = tk.Button(frame_registro, text="Guardar", command=guardar_paciente)
    btn_guardar.pack(pady=10, side="left")
    btn_cancelar = tk.Button(frame_registro, text="Cancelar", command=ventana_registro.destroy)
    btn_cancelar.pack(pady=10, side="right")

    centrar_ventana(ventana_registro, 4, 2, 3)


def cerrar_sesion():
    ventana_menu.destroy()
    login()

# Iniciar el programa con la ventana de login

login()
