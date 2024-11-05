import tkinter as tk
from tkinter import messagebox, ttk

import psycopg2


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
def centrar_ventana(ventana):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    ancho_ventana = ancho_pantalla // 2
    alto_ventana = alto_pantalla // 2
    x_pos = (ancho_pantalla - ancho_ventana) // 2
    y_pos = (alto_pantalla - alto_ventana) // 2
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

def cargar_logo(ventana):
    try:
        logo = tk.PhotoImage(file="icon.png")
        ventana.iconphoto(False, logo)
    except Exception as e:
        print("No se pudo cargar el icono:", e)

def refresh_table(treeview, table_name):
    # Borrar los datos actuales en el treeview
    for item in treeview.get_children():
        treeview.delete(item)
    
    # Re-cargar datos desde la base de datos
    connection, cursor = conectar_db()
    if connection and cursor:
        query = f"SELECT * FROM {table_name} ORDER BY codigo ASC"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            treeview.insert("", "end", values=row)
        
        cursor.close()
        connection.close()

# Ventana de login
def login():
    def check_login():
        user = entry_user.get()
        password = entry_pass.get()

        global username



        connection, cursor = conectar_db()
        
        if connection and cursor:
            if user == "admin" and password == "1234":
                ventana_login.destroy()
                username = "admin"
                abrir_menu_principal()

        
            else:
                #Conuslta verificar empleado
                cursor.execute("SELECT * FROM empleados where codigo =%s AND contrasena = %s", (user, password))
                empleado = cursor.fetchone()

                if empleado:
                    cursor.execute("SELECT nombre FROM empleados where codigo =%s", (user))
                    resultado = cursor.fetchone()
                    username = resultado[0] if resultado else ""
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
    
    centrar_ventana(ventana_login)
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
    
    title_text = "Bienvenido " + username

    label_title = tk.Label(frame_menu, text=title_text, font=("Arial", 24))
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
    
    centrar_ventana(ventana_menu)
    ventana_menu.mainloop()

# Ventana de empleados
def abrir_ventana_empleados():
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
    global tabla_empleados
    tabla_empleados = ttk.Treeview(tree_frame, columns=("codigo", "nombre", "direccion", "telefono", "fecha_nac", "sexo", "sueldo", "turno", "contrasena"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tabla_empleados.pack(fill="both", expand=True)
    
    # Configuración de las columnas
    tabla_empleados.heading("codigo", text="Código")
    tabla_empleados.heading("nombre", text="Nombre")
    tabla_empleados.heading("direccion", text="Dirección")
    tabla_empleados.heading("telefono", text="Teléfono")
    tabla_empleados.heading("fecha_nac", text="Fecha Nacimiento")
    tabla_empleados.heading("sexo", text="Sexo")
    tabla_empleados.heading("sueldo", text="Sueldo")
    tabla_empleados.heading("turno", text="Turno")
    tabla_empleados.heading("contrasena", text="Contraseña")
    
    # Ajustar el tamaño de las columnas
    tabla_empleados.column("codigo", width=80)
    tabla_empleados.column("nombre", width=150)
    tabla_empleados.column("direccion", width=200)
    tabla_empleados.column("telefono", width=100)
    tabla_empleados.column("fecha_nac", width=120)
    tabla_empleados.column("sexo", width=80)
    tabla_empleados.column("sueldo", width=100)
    tabla_empleados.column("turno", width=80)
    tabla_empleados.column("contrasena", width=120)
    
    # Asignar los scrollbars al tabla_empleados
    scrollbar_y.config(command=tabla_empleados.yview)
    scrollbar_x.config(command=tabla_empleados.xview)
    
    # Botones para registrar, editar y eliminar empleados
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Registrar", width=15, command=registrar_empleado)
    btn_registrar.pack(side="left", padx=10)
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15)
    btn_eliminar.pack(side="left", padx=10)

    btn_refresh = tk.Button(button_frame, text="Refrescar vista", width=15, command=lambda:refresh_table(tabla_empleados, "empleados"))
    btn_refresh.pack(side="right", padx=10)
    
    # Conectar y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM empleados ORDER BY codigo ASC")
        rows = cursor.fetchall()
        for row in rows:
            tabla_empleados.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_empleados)


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
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el empleado: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
    
    # Botón para guardar empleado
    btn_guardar = tk.Button(frame_registro, text="Guardar", command=guardar_empleado)
    btn_guardar.pack(pady=10)

    centrar_ventana(ventana_registro)

# Ventana de doctores
def abrir_ventana_doctores():
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
    tabla_doctores = ttk.Treeview(tree_frame, columns=("codigo", "nombre", "direccion", "telefono", "fecha_nac", "sexo", "especialidad", "contrasena"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tabla_doctores.pack(fill="both", expand=True)
    
    # Configuración de las columnas
    tabla_doctores.heading("codigo", text="Código")
    tabla_doctores.heading("nombre", text="Nombre")
    tabla_doctores.heading("direccion", text="Dirección")
    tabla_doctores.heading("telefono", text="Teléfono")
    tabla_doctores.heading("fecha_nac", text="Fecha Nacimiento")
    tabla_doctores.heading("sexo", text="Sexo")
    tabla_doctores.heading("especialidad", text="Especialidad")
    tabla_doctores.heading("contrasena", text="Contraseña")
    
    # Ajustar el tamaño de las columnas
    tabla_doctores.column("codigo", width=80)
    tabla_doctores.column("nombre", width=150)
    tabla_doctores.column("direccion", width=200)
    tabla_doctores.column("telefono", width=100)
    tabla_doctores.column("fecha_nac", width=120)
    tabla_doctores.column("sexo", width=80)
    tabla_doctores.column("especialidad", width=80)
    tabla_doctores.column("contrasena", width=120)
    
    # Asignar los scrollbars al Treeview
    scrollbar_y.config(command=tabla_doctores.yview)
    scrollbar_x.config(command=tabla_doctores.xview)
    
    # Botones para registrar, editar y eliminar doctores
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Registrar", width=15, command=registrar_doctor)
    btn_registrar.pack(side="left", padx=10)
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15)
    btn_eliminar.pack(side="left", padx=10)

    btn_refresh = tk.Button(button_frame, text="Refrescar vista", width=15, command=lambda:refresh_table(tabla_doctores, "doctores"))
    btn_refresh.pack(side="right", padx=10)
    
    # Conectar y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM doctores ORDER BY codigo ASC")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tabla_doctores.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_doctores)

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
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el doctor: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
    
    # Botón para guardar doctor
    btn_guardar = tk.Button(frame_registro, text="Guardar", command=guardar_doctor)
    btn_guardar.pack(pady=10)

    centrar_ventana(ventana_registro)

# Ventana de empleados
def abrir_ventana_pacientes():
    ventana_pacientes = tk.Toplevel()
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
    tabla_pacientes = ttk.Treeview(tree_frame, columns=("codigo", "nombre", "direccion", "telefono", "fecha_nac", "sexo", "edad", "estatura"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tabla_pacientes.pack(fill="both", expand=True)
    
    # Configuración de las columnas
    tabla_pacientes.heading("codigo", text="Código")
    tabla_pacientes.heading("nombre", text="Nombre")
    tabla_pacientes.heading("direccion", text="Dirección")
    tabla_pacientes.heading("telefono", text="Teléfono")
    tabla_pacientes.heading("fecha_nac", text="Fecha Nacimiento")
    tabla_pacientes.heading("sexo", text="Sexo")
    tabla_pacientes.heading("edad", text="Edad")
    tabla_pacientes.heading("estatura", text="Estatura")
    
    # Ajustar el tamaño de las columnas
    tabla_pacientes.column("codigo", width=80)
    tabla_pacientes.column("nombre", width=150)
    tabla_pacientes.column("direccion", width=200)
    tabla_pacientes.column("telefono", width=100)
    tabla_pacientes.column("fecha_nac", width=120)
    tabla_pacientes.column("sexo", width=80)
    tabla_pacientes.column("edad", width=80)
    tabla_pacientes.column("estatura", width=80)
    
    # Asignar los scrollbars al Treeview
    scrollbar_y.config(command=tabla_pacientes.yview)
    scrollbar_x.config(command=tabla_pacientes.xview)
    
    # Botones para registrar, editar y eliminar empleados
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Registrar", width=15, command=registrar_paciente)
    btn_registrar.pack(side="left", padx=10)
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15)
    btn_eliminar.pack(side="left", padx=10)

    btn_refresh = tk.Button(button_frame, text="Refrescar vista", width=15, command=lambda:refresh_table(tabla_pacientes, "pacientes"))
    btn_refresh.pack(side="right", padx=10)
    
    # Conectar y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM pacientes ORDER BY codigo ASC")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tabla_pacientes.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_pacientes)

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
        entry = tk.Entry(frame_registro)###
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
                        VALUES (%s, %s, %s, %s, %s, %s, %s  )
                    """
                    cursor.execute(query, tuple(valores))
                    connection.commit()
                    messagebox.showinfo("Éxito", "Paciente registrado exitosamente")
                    cursor.close()
                    connection.close()
                    ventana_registro.destroy()  # Cerrar la ventana de registro después de guardar
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar al paciente: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
    
    # Botón para guardar empleado
    btn_guardar = tk.Button(frame_registro, text="Guardar", command=guardar_paciente)
    btn_guardar.pack(pady=10)

    centrar_ventana(ventana_registro)



def cerrar_sesion():
    ventana_menu.destroy()
    login()

# Iniciar el programa con la ventana de login

login()
