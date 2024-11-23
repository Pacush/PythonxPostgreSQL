# Nucleo de diagnostico - Proyecto Final
# Equipo 6 - Bases de datos / 9am Ma, J / Sección D02 / 2024B
# Integrantes:
#   Sánchez Cuadro Hugo Leonardo.
#   Sánchez Naranjo José Alejandro.
#   Vargas Figueroa César Antonio.
#   Zúñiga Orozco Elías Alonso.

import tkinter as tk
from tkinter import messagebox, ttk

import psycopg2
from tkcalendar import Calendar

import pdf


# Función para establecer conexión con la base de datos
def conectar_db():
    try:
        # Se intenta conectar a la base de datos PostgreSQL con los parámetros definidos
        connection = psycopg2.connect(
            host='localhost',             # Dirección del servidor de base de datos
            user='postgres',              # Usuario de la base de datos
            password='12345',             # Contraseña del usuario
            database='NucleoDeDiagnostico', # Nombre de la base de datos
            port='5433'                   # Puerto del servidor
        )
        # Se crea un cursor para ejecutar consultas
        cursor = connection.cursor()
        return connection, cursor
    except Exception as ex:
        # Si ocurre un error, se muestra un mensaje y se retorna None
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {ex}")
        return None, None

# Función para centrar y redimensionar una ventana
def centrar_ventana(ventana, ancho_ventana_ratio, alto_ventana_ratio, pos_offset):
    # Obtiene las dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Calcula las dimensiones de la ventana según los ratios proporcionados
    ancho_ventana = ancho_pantalla // ancho_ventana_ratio
    alto_ventana = alto_pantalla // alto_ventana_ratio

    # Calcula la posición para centrar la ventana
    x_pos = (ancho_pantalla - ancho_ventana) // pos_offset
    y_pos = (alto_pantalla - alto_ventana) // pos_offset

    # Establece las dimensiones y posición calculadas
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")

# Función para cargar el logo de la ventana
def cargar_logo(ventana):
    try:
        # Intenta cargar una imagen como icono de la ventana
        logo = tk.PhotoImage(file="icon.png")
        ventana.iconphoto(False, logo)
    except Exception as e:
        print("No se pudo cargar el icono:", e)

# Función para actualizar los datos de una tabla mostrada en un Treeview
def refresh_table(treeview, tabla, doctor=False):
    # Elimina los datos actuales del Treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # Conecta a la base de datos para obtener datos actualizados
    connection, cursor = conectar_db()
    if connection and cursor:
        try:
            # Consulta dependiendo de la tabla y el contexto
            if tabla != "citas":
                cursor.execute(f"SELECT * FROM {tabla} ORDER BY codigo ASC")
            elif not doctor:
                cursor.execute("""
                    SELECT citas.codigo, pacientes.nombre, doctores.nombre, citas.fecha, citas.hora
                    FROM citas
                    INNER JOIN pacientes ON citas.codigo_paciente = pacientes.codigo
                    INNER JOIN doctores ON citas.codigo_doctor = doctores.codigo
                    ORDER BY codigo ASC
                """)
            else:
                cursor.execute(f"""
                    SELECT citas.codigo, pacientes.nombre, doctores.nombre, citas.fecha, citas.hora
                    FROM citas
                    INNER JOIN pacientes ON citas.codigo_paciente = pacientes.codigo
                    INNER JOIN doctores ON citas.codigo_doctor = doctores.codigo
                    WHERE citas.codigo_doctor = {user_id}
                    ORDER BY codigo ASC
                """)

            # Agrega las filas al Treeview
            rows = cursor.fetchall()
            for row in rows:
                treeview.insert("", "end", values=row)

        except Exception as e:
            print("Error al refrescar la tabla:", e)

        finally:
            cursor.close()
            connection.close()
    else:
        print("Fallo en la conexión a la base de datos")

# Función para cerrar una ventana y mostrar otra
def cancelar(ventana_cerrar, ventana_mostrar):
    ventana_cerrar.destroy()  # Cierra la ventana actual
    ventana_mostrar.lift()    # Trae al frente la ventana especificada

# Ventana de login
def login():
    def check_login():
        global user_id
        user_id = entry_user.get()  # Obtiene el texto ingresado en el campo de usuario
        password = entry_pass.get()  # Obtiene el texto ingresado en el campo de contraseña

        global username  # Variable global para almacenar el nombre del usuario logueado

        try:
            connection, cursor = conectar_db()
            if connection and cursor:
                # Si el usuario es administrador, verifica la contraseña directamente
                if user_id == "admin" and password == "1234":
                    ventana_login.destroy()
                    username = "admin"
                    menu_principal_admin()

                else:
                    # Verifica si el usuario es empleado
                    cursor.execute("SELECT * FROM empleados WHERE codigo = %s AND contrasena = %s", (user_id, password))
                    empleado = cursor.fetchone()

                    if empleado:
                        cursor.execute("SELECT nombre FROM empleados WHERE codigo = %s", (user_id,))
                        resultado = cursor.fetchone()
                        username = resultado[0] if resultado else ""
                        ventana_login.destroy()
                        menu_principal_empleado()

                    else:
                        # Verifica si el usuario es doctor
                        cursor.execute("SELECT * FROM doctores WHERE codigo = %s AND contrasena = %s", (user_id, password))
                        doctor = cursor.fetchone()

                        if doctor:
                            cursor.execute("SELECT nombre FROM doctores WHERE codigo = %s", (user_id,))
                            resultado = cursor.fetchone()
                            username = resultado[0] if resultado else ""
                            ventana_login.destroy()
                            menu_principal_doctor()
                        else:
                            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

                cursor.close()
                connection.close()

            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")

        except Exception as e:
            print(e)
            messagebox.showerror("Error", "No fue posible cargar la sesión correctamente")

    # Creación de la ventana de login
    ventana_login = tk.Tk()
    ventana_login.title("Login")

    cargar_logo(ventana_login)  # Carga el logo de la ventana

    # Configuración de la interfaz del login
    frame_login = tk.Frame(ventana_login)
    frame_login.pack(expand=True, fill="both")

    label_user = tk.Label(frame_login, text="Usuario:")
    label_user.pack(pady=5)

    entry_user = tk.Entry(frame_login)
    entry_user.pack(pady=5)

    label_pass = tk.Label(frame_login, text="Contraseña:")
    label_pass.pack(pady=5)

    entry_pass = tk.Entry(frame_login, show="*")  # Campo para la contraseña (oculta los caracteres)
    entry_pass.pack(pady=5)

    # Botón para iniciar sesión
    btn_login = tk.Button(frame_login, text="Login", command=check_login)
    btn_login.pack(pady=10)

    # Centrar y mostrar la ventana de login
    centrar_ventana(ventana_login, 5, 3, 2)
    ventana_login.mainloop()

def menu_principal_admin():
    # Carga de la ventana, contenedores y botones
    global ventana_menu
    ventana_menu = tk.Tk()
    ventana_menu.title("Gestor de registros")
    cargar_logo(ventana_menu)
    
    frame_centrado = tk.Frame(ventana_menu)
    frame_centrado.pack(expand=True)

    frame_menu = tk.Frame(frame_centrado)
    frame_menu.grid(row=0, column=0, padx=20, pady=2)
    
    title_text = "Bienvenido " + username
    
    label_title = tk.Label(frame_menu, text=title_text, font=("Arial", 24))
    label_title.grid(row=0, column=0, columnspan=2, pady=2)
    
    btn1 = tk.Button(frame_menu, text="Empleados", command=abrir_ventana_empleados, width=20)
    btn1.grid(row=1, column=0, padx=10, pady=2, sticky="w")
    
    btn2 = tk.Button(frame_menu, text="Doctores", command=abrir_ventana_doctores , width=20)
    btn2.grid(row=2, column=0, padx=10, pady=2, sticky="w")

    btn3 = tk.Button(frame_menu, text="Pacientes", command=abrir_ventana_pacientes, width=20)
    btn3.grid(row=3, column=0, padx=10, pady=2, sticky="w")
    
    btn4 = tk.Button(frame_menu, text="Citas", width=20, command=abrir_ventana_citas_empleados)
    btn4.grid(row=4, column=0, padx=10, pady=2, sticky="w")
    
    btn5 = tk.Button(frame_menu, text="Medicamentos", width=20, command=abrir_ventana_medicamentos)
    btn5.grid(row=5, column=0, padx=10, pady=2, sticky="w")
    
    btn6 = tk.Button(frame_menu, text="Cerrar sesión", width=20, command=cerrar_sesion)
    btn6.grid(row=6, column=0, padx=10, pady=2, sticky="w")
    
    # Carga del logo
    logo_img = tk.PhotoImage(file="logo2.png")
    label_logo = tk.Label(frame_menu, image=logo_img)
    label_logo.grid(row=1, column=1, rowspan=6, padx=20, pady=10, sticky="e")
    
    centrar_ventana(ventana_menu, 2, 2, 2)
    ventana_menu.mainloop()

def menu_principal_empleado():
    # Carga de la ventana, contenedores y botones
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

    btn1 = tk.Button(frame_menu, text="Pacientes", command=abrir_ventana_pacientes, width=20)
    btn1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    btn2 = tk.Button(frame_menu, text="Citas", width=20, command=abrir_ventana_citas_empleados)
    btn2.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    
    btn3 = tk.Button(frame_menu, text="Cerrar sesión", width=20, command=cerrar_sesion)
    btn3.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    
    logo_img = tk.PhotoImage(file="logo2.png")
    label_logo = tk.Label(frame_menu, image=logo_img)
    label_logo.grid(row=1, column=1, rowspan=3, padx=20, pady=10, sticky="e")
    
    centrar_ventana(ventana_menu, 2, 2, 2)
    ventana_menu.mainloop()

def menu_principal_doctor():
    
    # Carga de la ventana, contenedores y botones
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

    btn1 = tk.Button(frame_menu, text="Pacientes", command=abrir_ventana_pacientes_doctores, width=20)
    btn1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    btn2 = tk.Button(frame_menu, text="Citas", width=20, command=abrir_ventana_citas_doctores)
    btn2.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    
    btn3 = tk.Button(frame_menu, text="Cerrar sesión", width=20, command=cerrar_sesion)
    btn3.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    
    logo_img = tk.PhotoImage(file="logo2.png")
    label_logo = tk.Label(frame_menu, image=logo_img)
    label_logo.grid(row=1, column=1, rowspan=3, padx=20, pady=10, sticky="e")
    
    centrar_ventana(ventana_menu, 2, 2, 2)
    ventana_menu.mainloop()

# Ventana de empleados
def abrir_ventana_empleados():
    
    # Carga de la ventana, contenedores y botones
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
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15, command=editar_empleado)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15, command=eliminar_empleado)
    btn_eliminar.pack(side="left", padx=10)
    
    
    btn_refresh = tk.Button(button_frame, text="Refresh", width=15, command=lambda: refresh_table(tablaEmpleados, "empleados"))
    btn_refresh.pack(side="right", padx=10)
    
    
    # Conectar con la BD y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM empleados ORDER BY codigo ASC")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tablaEmpleados.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_empleados, 2, 2, 3)

def abrir_ventana_pacientes():
    
    # Carga de la ventana, contenedores y botones
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
    
    # Definir columnas de la tabla pacientes
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
    
    # Botones para registrar, editar y eliminar pacientes
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Registrar", width=15, command=registrar_paciente)
    btn_registrar.pack(side="left", padx=10)
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15, command=editar_paciente)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15, command=abrir_ventana_eliminar_paciente)
    btn_eliminar.pack(side="left", padx=10)
    
    btn_refresh = tk.Button(button_frame, text="Refresh", width=15, command=lambda: refresh_table(tablaPacientes, "pacientes"))
    btn_refresh.pack(side="right", padx=10)
    
    # Conectar con la BD y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM pacientes ORDER BY codigo ASC")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tablaPacientes.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_pacientes, 2, 2, 3)

def abrir_ventana_doctores():
    
    # Carga de la ventana, contenedores y botones
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
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15, command=editar_doctor)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15, command=eliminar_doctor)
    btn_eliminar.pack(side="left", padx=10)
    
    btn_refresh = tk.Button(button_frame, text="Refresh", width=15, command=lambda: refresh_table(tablaDoctores, "doctores"))
    btn_refresh.pack(side="right", padx=10)
    
    # Conectar con la BD y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM doctores ORDER BY codigo ASC")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tablaDoctores.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_doctores, 2, 2, 3)

def registrar_empleado():
    
    # Carga de la ventana, contenedores y botones
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
        
        # Obtener los valores de los campos
        valores = [entry.get() for entry in entries]
        
        # Si se ingresaron valores en los campos, se manda la sentencia INSERT SQL a la BD.
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
                    # Cerrar ventana de registro y mostrar la tabla
                    ventana_registro.destroy()
                    ventana_empleados.lift()
                    
                #Si no es valido o hay un error en la conexion, tira error dependiendo del tipo
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                    ventana_registro.destroy()
                    ventana_empleados.lift()
            except Exception as e:
                print(e)
                messagebox.showerror("Error", f"No se pudo registrar el empleado")
                ventana_registro.lift()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            ventana_registro.lift()
    
    # Al finalizar se refresca la tabla
    refresh_table(tablaEmpleados, "empleados")
    
    # Botones para guardar y cancelar
    btn_guardar = tk.Button(frame_registro, text="Guardar", command=guardar_empleado)
    btn_guardar.pack(pady=10, side="left")
    btn_cancelar = tk.Button(frame_registro, text="Cancelar", command=lambda: cancelar(ventana_registro, ventana_empleados))
    btn_cancelar.pack(pady=10, side="right")
    
    centrar_ventana(ventana_registro, 4, 2, 3)

def eliminar_empleado():
    # Crear una ventana para seleccionar la cita a editar
    global ventana_eliminar_empleado
    ventana_eliminar_empleado = tk.Toplevel()
    ventana_eliminar_empleado.title("Eliminar Empleado")
    frame_eliminar = tk.Frame(ventana_eliminar_empleado)
    frame_eliminar.pack(padx=10, pady=10)
    cargar_logo(ventana_eliminar_empleado)
    centrar_ventana(ventana_eliminar_empleado, 7, 7, 3)

    # Conectar y obtener los códigos de citas existentes
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM empleados ORDER BY codigo ASC")
            empleados = cursor.fetchall()
            lista_empleados = [str(empleado[0]) for empleado in empleados]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"No se pudo cargar los datos de los empleados")
        return

    # Mostrar la lista de citas
    tk.Label(frame_eliminar, text="Seleccione el ID del empleado a eliminar:").pack(pady=5)
    combo_empleados = ttk.Combobox(frame_eliminar, values=lista_empleados)
    combo_empleados.pack()

    # Botón para continuar con la edición
    tk.Button(frame_eliminar, text="Continuar", command=lambda: continuar_eliminacion_empleado(combo_empleados.get())).pack(pady=20)

    def continuar_eliminacion_empleado(codigo_empleado):
        if not codigo_empleado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un codigo de empleado.")
            return
        
        try:
            connection, cursor = conectar_db()
            if connection and cursor:

                confirmacion = messagebox.askyesno(
                    "Confirmar Eliminacion",
                    f"¿Deseas eliminar al empleado {codigo_empleado}?"
                )
                if confirmacion:
                    cursor.execute(f"DELETE FROM empleados WHERE codigo = {codigo_empleado};")
                    connection.commit()
                    messagebox.showinfo("Empleado Eliminado", "El empleado ha sido eliminado exitosamente.")
                    ventana_empleados.lift()
                    refresh_table(tablaEmpleados, "empleados")
                
                    cursor.close()
                    connection.close()

            else:
                raise Exception("No se pudo conectar a la base de datos")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"No se pudo cargar los datos de los pacientes")
            return

def editar_empleado():

    ventana_editar_empleado = tk.Toplevel()
    ventana_editar_empleado.title("Editar Empleado")
    frame_editar = tk.Frame(ventana_editar_empleado)
    frame_editar.pack(padx=10, pady=10)
    cargar_logo(ventana_editar_empleado)
    centrar_ventana(ventana_editar_empleado, 7, 7, 3)

    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM empleados ORDER BY codigo ASC")
            empleados = cursor.fetchall()
            lista_empleados = [str(empleado[0]) for empleado in empleados]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"No se pudo cargar los datos de los empleados")
        return

    # Mostrar la lista de citas
    tk.Label(frame_editar, text="Seleccione el ID del empleado a editar:").pack(pady=5)
    combo_empleados = ttk.Combobox(frame_editar, values=lista_empleados)
    combo_empleados.pack()

    # Botón para continuar con la edición
    tk.Button(frame_editar, text="Continuar", command=lambda: continuar_edicion_empleado(combo_empleados.get())).pack(pady=20)

    def continuar_edicion_empleado(codigo_empleado):
        ventana_editar_empleado.destroy()
        ventana_edicion = tk.Toplevel()
        ventana_edicion.title("Editar información del empleado")
        cargar_logo(ventana_edicion)
        centrar_ventana(ventana_edicion, 3, 2, 2)
    
        frame_edicion = tk.Frame(ventana_edicion)
        frame_edicion.pack(padx=10, pady=10)

        labels = ["Nombre", "Dirección", "Teléfono", "Fecha Nac (YYYY-MM-DD)", "Sexo", "Sueldo", "Turno", "Contraseña"]
        entries = []

        try:
            connection, cursor = conectar_db()
            if connection and cursor:
                cursor.execute("SELECT nombre, direccion, telefono, fecha_nac, sexo, sueldo, turno, contrasena FROM empleados WHERE codigo = %s", (codigo_empleado,))
                empleado = cursor.fetchone()
            
                if empleado:
                    # Rellenar las entradas con la información actual
                    for i, label_text in enumerate(labels):
                        label = tk.Label(frame_edicion, text=label_text)
                        label.pack(pady=2)

                        entry = tk.Entry(frame_edicion)
                        entry.pack(pady=2)

                        # Establecer valor inicial desde la base de datos
                        entry.insert(0, str(empleado[i]))
                        entries.append(entry)
                else:
                    messagebox.showerror("Error", "No se encontró al empleado")
                    ventana_edicion.destroy()
                    return
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                ventana_edicion.destroy()
                return
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Ocurrió un error al obtener la información del paciente")
            ventana_edicion.destroy()
            return

        def guardar_empleado():
            # Recuperar los valores de los campos
            valores = [entry.get() for entry in entries]
            if all(valores):
                try:
                    connection, cursor = conectar_db()
                    if connection and cursor:

                        confirmacion = messagebox.askyesno(
                        "Confirmar Edición",
                        f"¿Deseas actualizar la información del empleado con código {codigo_empleado}?"
                        )
                        if confirmacion:

                            sql_update = """
                            UPDATE empleados
                            SET nombre = %s, direccion = %s, telefono = %s, fecha_nac = %s, sexo = %s, sueldo = %s, turno = %s, contrasena = %s WHERE codigo = %s
                            """
                            cursor.execute(sql_update, (*valores, codigo_empleado))

                            connection.commit()
                            messagebox.showinfo("Empleado Actualizado", "La información del empleado ha sido actualizada exitosamente.")
                            ventana_edicion.destroy()
                            ventana_empleados.lift()
                            refresh_table(tablaEmpleados, "empleados")

                    else:
                        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                        ventana_edicion.destroy()
                        ventana_empleados.lift()
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", f"No se pudo editar la informacin del empleado")
                    ventana_edicion.lift()
                
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                ventana_edicion.lift()
            
        refresh_table(tablaEmpleados, "empleados")
        # Botón para guardar doctor
        btn_guardar = tk.Button(frame_edicion, text="Guardar", command=guardar_empleado)
        btn_guardar.pack(pady=10, side="left")
        btn_cancelar = tk.Button(frame_edicion, text="Cancelar", command=lambda: cancelar(ventana_edicion, ventana_empleados))
        btn_cancelar.pack(pady=10, side="right")

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
    btn_cancelar = tk.Button(frame_registro, text="Cancelar", command=lambda: cancelar(ventana_registro, ventana_doctores))
    btn_cancelar.pack(pady=10, side="right")

    centrar_ventana(ventana_registro, 4, 2, 3)

def editar_doctor():
    # Ventana para registrar nuevo empleado

    ventana_editar_doctor = tk.Toplevel()
    ventana_editar_doctor.title("Editar Doctor")
    frame_editar = tk.Frame(ventana_editar_doctor)
    frame_editar.pack(padx=10, pady=10)
    cargar_logo(ventana_editar_doctor)
    centrar_ventana(ventana_editar_doctor, 7, 7, 3)

    # Conectar y obtener los códigos de citas existentes
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM doctores ORDER BY codigo ASC")
            doctores = cursor.fetchall()
            lista_doctores = [str(doctor[0]) for doctor in doctores]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"No se pudo cargar los datos de los doctores")
        return

    # Mostrar la lista de citas
    tk.Label(frame_editar, text="Seleccione el ID del doctor a editar:").pack(pady=5)
    combo_doctores = ttk.Combobox(frame_editar, values=doctores)
    combo_doctores.pack()

    # Botón para continuar con la edición
    tk.Button(frame_editar, text="Continuar", command=lambda: continuar_edicion_doctor(combo_doctores.get())).pack(pady=20)

    def continuar_edicion_doctor(codigo_doctor):
        ventana_editar_doctor.destroy()
        ventana_edicion = tk.Toplevel()
        ventana_edicion.title("Editar información del doctor")
        cargar_logo(ventana_edicion)
        centrar_ventana(ventana_edicion, 3, 2, 2)
    
        frame_edicion = tk.Frame(ventana_edicion)
        frame_edicion.pack(padx=10, pady=10)

        labels = ["Nombre", "Dirección", "Teléfono", "Fecha Nac (YYYY-MM-DD)", "Sexo", "Especialidad", "Contraseña"]
        entries = []

        try:
            connection, cursor = conectar_db()
            if connection and cursor:
                cursor.execute("SELECT nombre, direccion, telefono, fecha_nac, sexo, especialidad, contrasena FROM doctores WHERE codigo = %s", (codigo_doctor,))
                doctor = cursor.fetchone()
            
                if doctor:
                    # Rellenar las entradas con la información actual
                    for i, label_text in enumerate(labels):
                        label = tk.Label(frame_edicion, text=label_text)
                        label.pack(pady=2)

                        entry = tk.Entry(frame_edicion)
                        entry.pack(pady=2)

                        # Establecer valor inicial desde la base de datos
                        entry.insert(0, str(doctor[i]))
                        entries.append(entry)
                else:
                    messagebox.showerror("Error", "No se encontró al doctor")
                    ventana_edicion.destroy()
                    return
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                ventana_edicion.destroy()
                return
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Ocurrió un error al obtener la información del doctor")
            ventana_edicion.destroy()
            return

        def guardar_doctor():
            # Recuperar los valores de los campos
            valores = [entry.get() for entry in entries]
            if all(valores):
                try:
                    connection, cursor = conectar_db()
                    if connection and cursor:

                        confirmacion = messagebox.askyesno(
                        "Confirmar Edición",
                        f"¿Deseas actualizar la información del doctor con código {codigo_doctor}?"
                        )
                        if confirmacion:

                            sql_update = """
                            UPDATE doctores
                            SET nombre = %s, direccion = %s, telefono = %s, fecha_nac = %s,
                                sexo = %s, especialidad = %s, contrasena = %s
                            WHERE codigo = %s
                            """
                            cursor.execute(sql_update, (*valores, codigo_doctor))

                            connection.commit()
                            messagebox.showinfo("Doctor Actualizado", "La información del doctor ha sido actualizada exitosamente.")
                            ventana_edicion.destroy()
                            ventana_doctores.lift()
                            refresh_table(tablaDoctores, "doctores")

                    else:
                        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                        ventana_edicion.destroy()
                        ventana_doctores.lift()
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", f"No se pudo editar la informacin del paciente")
                    ventana_edicion.lift()
                
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                ventana_edicion.lift()
            
        refresh_table(tablaDoctores, "doctores")
        # Botón para guardar doctor
        btn_guardar = tk.Button(frame_edicion, text="Guardar", command=guardar_doctor)
        btn_guardar.pack(pady=10, side="left")
        btn_cancelar = tk.Button(frame_edicion, text="Cancelar", command=lambda: cancelar(ventana_edicion, ventana_doctores))
        btn_cancelar.pack(pady=10, side="right")

def eliminar_doctor():
    # Crear una ventana para seleccionar la cita a editar
    ventana_eliminar_doctor = tk.Toplevel()
    ventana_eliminar_doctor.title("Eliminar Empleado")
    frame_eliminar = tk.Frame(ventana_eliminar_doctor)
    frame_eliminar.pack(padx=10, pady=10)
    cargar_logo(ventana_eliminar_doctor)
    centrar_ventana(ventana_eliminar_doctor, 7, 7, 3)

    # Conectar y obtener los códigos de citas existentes
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM doctores ORDER BY codigo ASC")
            doctores = cursor.fetchall()
            lista_doctores = [str(doctor[0]) for doctor in doctores]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"No se pudo cargar los datos de los doctores")
        return

    # Mostrar la lista de citas
    tk.Label(frame_eliminar, text="Seleccione el ID del doctor a eliminar:").pack(pady=5)
    combo_doctores = ttk.Combobox(frame_eliminar, values=lista_doctores)
    combo_doctores.pack()

    # Botón para continuar con la edición
    tk.Button(frame_eliminar, text="Continuar", command=lambda: continuar_eliminacion_doctor(combo_doctores.get())).pack(pady=20)

    def continuar_eliminacion_doctor(codigo_doctor):
        if not codigo_doctor:
            messagebox.showwarning("Advertencia", "Debe seleccionar un codigo de doctor.")
            return
        
        try:
            connection, cursor = conectar_db()
            if connection and cursor:

                confirmacion = messagebox.askyesno(
                    "Confirmar Eliminacion",
                    f"¿Deseas eliminar al doctor {codigo_doctor}?"
                )
                if confirmacion:
                    cursor.execute(f"DELETE FROM doctores WHERE codigo = {codigo_doctor};")
                    connection.commit()
                    messagebox.showinfo("Doctor Eliminado", "El empldoctoreado ha sido eliminado exitosamente.")
                    ventana_doctores.lift()
                    refresh_table(tablaDoctores, "doctores")
                
                    cursor.close()
                    connection.close()

            else:
                raise Exception("No se pudo conectar a la base de datos")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"No se pudo cargar los datos de los doctores")
            return

def abrir_ventana_eliminar_paciente():
    # Crear una ventana para seleccionar la cita a editar
    global ventana_eliminar_paciente
    ventana_eliminar_paciente = tk.Toplevel()
    ventana_eliminar_paciente.title("Eliminar Paciente")
    frame_editar = tk.Frame(ventana_eliminar_paciente)
    frame_editar.pack(padx=10, pady=10)
    cargar_logo(ventana_eliminar_paciente)
    centrar_ventana(ventana_eliminar_paciente, 7, 7, 3)

    # Conectar y obtener los códigos de citas existentes
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM pacientes")
            citas = cursor.fetchall()
            lista_citas = [str(cita[0]) for cita in citas]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"No se pudo cargar los datos de las citas")
        return

    # Mostrar la lista de citas
    tk.Label(frame_editar, text="Seleccione el ID del paciente a eliminar:").pack(pady=5)
    combo_pacientes = ttk.Combobox(frame_editar, values=lista_citas)
    combo_pacientes.pack()

    # Botón para continuar con la edición
    tk.Button(frame_editar, text="Continuar", command=lambda: continuar_eliminacion_paciente(combo_pacientes.get())).pack(pady=20)

    def continuar_eliminacion_paciente(codigo_paciente):
        if not codigo_paciente:
            messagebox.showwarning("Advertencia", "Debe seleccionar una cita.")
            return
        
        try:
            connection, cursor = conectar_db()
            if connection and cursor:

                confirmacion = messagebox.askyesno(
                    "Confirmar Eliminacion",
                    f"¿Deseas eliminar al paciente {codigo_paciente}?"
                )
                if confirmacion:
                    cursor.execute(f"DELETE FROM pacientes WHERE codigo = {codigo_paciente};")
                    connection.commit()
                    messagebox.showinfo("Paciente Eliminado", "El paciente ha sido eliminado exitosamente.")
                    ventana_pacientes.lift()
                    refresh_table(tablaPacientes, "citas")
                

                    cursor.close()
                    connection.close()

            else:
                raise Exception("No se pudo conectar a la base de datos")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"No se pudo cargar los datos de los pacientes")
            return

def abrir_ventana_pacientes_doctores():
    global ventana_pacientes_doctor
    ventana_pacientes_doctor= tk.Toplevel()
    ventana_pacientes_doctor.title("Pacientes")
    cargar_logo(ventana_pacientes_doctor)
    
    frame_principal = tk.Frame(ventana_pacientes_doctor)
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
    
    centrar_ventana(ventana_pacientes_doctor, 2, 2, 3)

def asignar_consulta():
    global ventana_asignar_consulta
    ventana_asignar_consulta = tk.Toplevel()
    ventana_asignar_consulta.title("Asignar consulta")
    frame_asignar_consulta = tk.Frame(ventana_asignar_consulta)
    frame_asignar_consulta.pack(padx=10, pady=10, fill="both", expand=True)
    centrar_ventana(ventana_asignar_consulta, 3, 3, 3)
    cargar_logo(ventana_asignar_consulta)


    # Conectar y obtener nombres de pacientes y doctores
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            # Obtener pacientes
            cursor.execute(f"SELECT citas.codigo FROM citas INNER JOIN pacientes ON citas.codigo_paciente = pacientes.codigo INNER JOIN doctores ON citas.codigo_doctor = doctores.codigo WHERE citas.codigo_doctor = {user_id} ORDER BY codigo ASC;")
            citas = cursor.fetchall()

            # Obtener doctores (incluyendo código y nombre)
            cursor.execute("SELECT codigo, nombre FROM medicamentos")
            medicamentos = cursor.fetchall()
            nombres_medicamentos = [row[1] for row in medicamentos]  # Lista de nombres
            global medicamentos_dict
            medicamentos_dict = {row[1]: row[0] for row in medicamentos}  # Diccionario {nombre: código}

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        print (e)
        messagebox.showerror("Error", f"No se pudo cargar los datos")
        return

    # Etiquetas y listas desplegables para seleccionar paciente y doctor
    tk.Label(frame_asignar_consulta, text="Seleccione el ID de la cita:").pack(pady=5)
    combo_citas = ttk.Combobox(frame_asignar_consulta, values=citas, width=30)
    combo_citas.pack()

    tk.Label(frame_asignar_consulta, text="Seleccione el medicamento:").pack(pady=5)
    combo_medicamentos = ttk.Combobox(frame_asignar_consulta, values=nombres_medicamentos, width=30)
    combo_medicamentos.pack()
    
    label_diagnostico = tk.Label(frame_asignar_consulta, text="Diagnostico")
    label_diagnostico.pack(pady=2)
    entry_diagnostico = tk.Text(frame_asignar_consulta, height=10)
    entry_diagnostico.pack(pady=2)

    def continuar_asignacion_consulta():
        cita_seleccionada = combo_citas.get()
        diagnostico = entry_diagnostico.get("1.0", tk.END)
        medicamento_seleccionado = medicamentos_dict.get(combo_medicamentos.get())
        
        
        valores = [cita_seleccionada, diagnostico, medicamento_seleccionado]
        if all(valores):
            try:
                connection, cursor = conectar_db()
                if connection and cursor:
                    query = """
                        INSERT INTO consultas (codigo_cita, diagnostico, codigo_medicamento)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, tuple(valores))
                    
                    if not pdf.consulta2pdf(cita_seleccionada, diagnostico, medicamento_seleccionado):
                        messagebox.showerror("Error", "No se pudo imprimir la consulta")
                    
                    connection.commit()
                    messagebox.showinfo("Éxito", "Consulta registrada exitosamente")
                    cursor.close()
                    connection.close()
                    ventana_asignar_consulta.destroy()  # Cerrar la ventana de registro después de guardar
                    ventana_citas_doctores.lift()
                    
                    
                    
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                    ventana_asignar_consulta.destroy()
                    ventana_citas_doctores.lift()

                    
            except Exception as e:
                print(e)
                messagebox.showerror("Error", f"No se pudo registrar la consulta")
                ventana_asignar_consulta.lift()
                
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            ventana_asignar_consulta.lift()
    
    # Botón para continuar con la consulta
    tk.Button(frame_asignar_consulta, text="Continuar", command=continuar_asignacion_consulta).pack(pady=20)
     
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
    btn_cancelar = tk.Button(frame_registro, text="Cancelar", command=lambda: cancelar(ventana_registro, ventana_pacientes))
    btn_cancelar.pack(pady=10, side="right")

    centrar_ventana(ventana_registro, 4, 2, 3)

def editar_paciente():
    # Ventana para registrar nuevo empleado

    global ventana_editar_paciente
    ventana_editar_paciente = tk.Toplevel()
    ventana_editar_paciente.title("Editar Paciente")
    frame_editar = tk.Frame(ventana_editar_paciente)
    frame_editar.pack(padx=10, pady=10)
    cargar_logo(ventana_editar_paciente)
    centrar_ventana(ventana_editar_paciente, 7, 7, 3)

    # Conectar y obtener los códigos de citas existentes
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM pacientes ORDER BY codigo ASC")
            pacientes = cursor.fetchall()
            lista_citas = [str(paciente[0]) for paciente in pacientes]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"No se pudo cargar los datos de los pacientes")
        return

    # Mostrar la lista de citas
    tk.Label(frame_editar, text="Seleccione el ID del paciente a editar:").pack(pady=5)
    combo_pacientes = ttk.Combobox(frame_editar, values=lista_citas)
    combo_pacientes.pack()

    # Botón para continuar con la edición
    tk.Button(frame_editar, text="Continuar", command=lambda: continuar_edicion_paciente(combo_pacientes.get())).pack(pady=20)

    def continuar_edicion_paciente(codigo_paciente):
        ventana_editar_paciente.destroy()
        ventana_edicion = tk.Toplevel()
        ventana_edicion.title("Editar información del paciente")
        cargar_logo(ventana_edicion)
        centrar_ventana(ventana_edicion, 3, 2, 2)
    
        frame_edicion = tk.Frame(ventana_edicion)
        frame_edicion.pack(padx=10, pady=10)

        labels = ["Nombre", "Dirección", "Teléfono", "Fecha Nac (YYYY-MM-DD)", "Sexo", "Edad", "Estatura (metros)"]
        entries = []

        try:
            connection, cursor = conectar_db()
            if connection and cursor:
                cursor.execute("SELECT nombre, direccion, telefono, fecha_nac, sexo, edad, estatura FROM pacientes WHERE codigo = %s", (codigo_paciente,))
                paciente = cursor.fetchone()
            
                if paciente:
                    # Rellenar las entradas con la información actual
                    for i, label_text in enumerate(labels):
                        label = tk.Label(frame_edicion, text=label_text)
                        label.pack(pady=2)

                        entry = tk.Entry(frame_edicion)
                        entry.pack(pady=2)

                        # Establecer valor inicial desde la base de datos
                        entry.insert(0, str(paciente[i]))
                        entries.append(entry)
                else:
                    messagebox.showerror("Error", "No se encontró al paciente")
                    ventana_edicion.destroy()
                    return
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                ventana_edicion.destroy()
                return
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Ocurrió un error al obtener la información del paciente")
            ventana_edicion.destroy()
            return

        def guardar_paciente():
            # Recuperar los valores de los campos
            valores = [entry.get() for entry in entries]
            if all(valores):
                try:
                    connection, cursor = conectar_db()
                    if connection and cursor:

                        confirmacion = messagebox.askyesno(
                        "Confirmar Edición",
                        f"¿Deseas actualizar la información del paciente con código {codigo_paciente}?"
                        )
                        if confirmacion:

                            sql_update = """
                            UPDATE pacientes
                            SET nombre = %s, direccion = %s, telefono = %s, fecha_nac = %s, 
                                sexo = %s, edad = %s, estatura = %s
                            WHERE codigo = %s
                            """
                            cursor.execute(sql_update, (*valores, codigo_paciente))

                            connection.commit()
                            messagebox.showinfo("Paciente Actualizado", "La información del paciente ha sido actualizada exitosamente.")
                            ventana_edicion.destroy()
                            ventana_pacientes.lift()
                            refresh_table(tablaPacientes, "pacientes")

                    else:
                        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                        ventana_edicion.destroy()
                        ventana_pacientes.lift()
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", f"No se pudo editar la informacin del paciente")
                    ventana_edicion.lift()
                
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                ventana_edicion.lift()
            
        refresh_table(tablaPacientes, "pacientes")
        # Botón para guardar doctor
        btn_guardar = tk.Button(frame_edicion, text="Guardar", command=guardar_paciente)
        btn_guardar.pack(pady=10, side="left")
        btn_cancelar = tk.Button(frame_edicion, text="Cancelar", command=lambda: cancelar(ventana_edicion, ventana_pacientes))
        btn_cancelar.pack(pady=10, side="right")

def abrir_ventana_citas_empleados():
    global ventana_citas_empleados
    ventana_citas_empleados = tk.Toplevel()
    ventana_citas_empleados.title("Citas")
    cargar_logo(ventana_citas_empleados)
    
    frame_principal = tk.Frame(ventana_citas_empleados)
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
    global tablaCitasEmpleados
    tablaCitasEmpleados = ttk.Treeview(tree_frame, columns=("codigo", "paciente", "doctor", "fecha", "hora"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tablaCitasEmpleados.pack(fill="both", expand=True)
    
    # Configuración de las columnas
    tablaCitasEmpleados.heading("codigo", text="Código de cita")
    tablaCitasEmpleados.heading("paciente", text="Paciente")
    tablaCitasEmpleados.heading("doctor", text="Doctor")
    tablaCitasEmpleados.heading("fecha", text="Fecha")
    tablaCitasEmpleados.heading("hora", text="Hora")
    
    # Ajustar el tamaño de las columnas
    tablaCitasEmpleados.column("codigo", width=50)
    tablaCitasEmpleados.column("paciente", width=150)
    tablaCitasEmpleados.column("doctor", width=150)
    tablaCitasEmpleados.column("fecha", width=80)
    tablaCitasEmpleados.column("hora", width=80)
    
    # Asignar los scrollbars al Treeview
    scrollbar_y.config(command=tablaCitasEmpleados.yview)
    scrollbar_x.config(command=tablaCitasEmpleados.xview)
    
    # Botones para registrar, editar y eliminar empleados
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Registrar", width=15, command=abrir_ventana_registrar_cita)
    btn_registrar.pack(side="left", padx=10)
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15, command=abrir_ventana_editar_cita)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15, command=abrir_ventana_eliminar_cita)
    btn_eliminar.pack(side="left", padx=10)
    
    btn_refresh = tk.Button(button_frame, text="Refresh", width=15, command=lambda: refresh_table(tablaCitasEmpleados, "citas"))
    btn_refresh.pack(side="right", padx=10)
    
    # Conectar y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT citas.codigo, pacientes.nombre, doctores.nombre, citas.fecha, citas.hora FROM citas INNER JOIN pacientes ON citas.codigo_paciente = pacientes.codigo INNER JOIN doctores ON citas.codigo_doctor = doctores.codigo ORDER BY codigo ASC;")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tablaCitasEmpleados.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_citas_empleados, 2, 2, 3)

def abrir_ventana_registrar_cita():
    # Crear una nueva ventana más pequeña para registrar citas
    global ventana_registrar_cita
    ventana_registrar_cita = tk.Toplevel()
    ventana_registrar_cita.title("Registrar Cita")
    cargar_logo(ventana_registrar_cita)

    frame_registro = tk.Frame(ventana_registrar_cita)
    frame_registro.pack(padx=10, pady=10, fill="both", expand=True)


    # Conectar y obtener nombres de pacientes y doctores
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            # Obtener pacientes
            cursor.execute("SELECT codigo, nombre FROM pacientes")
            pacientes = cursor.fetchall()
            nombres_pacientes = [row[1] for row in pacientes]
            global pacientes_dic
            pacientes_dic = {row[1]: row[0] for row in pacientes}

            # Obtener doctores (incluyendo código y nombre)
            cursor.execute("SELECT codigo, nombre FROM doctores")
            doctores = cursor.fetchall()
            nombres_doctores = [row[1] for row in doctores]  # Lista de nombres
            global doctores_dict
            doctores_dict = {row[1]: row[0] for row in doctores}  # Diccionario {nombre: código}

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")
        return

    # Etiquetas y listas desplegables para seleccionar paciente y doctor
    tk.Label(frame_registro, text="Seleccione Paciente:").pack(pady=5)
    combo_pacientes = ttk.Combobox(frame_registro, values=nombres_pacientes, width=30)
    combo_pacientes.pack()

    tk.Label(frame_registro, text="Seleccione Doctor:").pack(pady=5)
    combo_doctores = ttk.Combobox(frame_registro, values=nombres_doctores, width=30)
    combo_doctores.pack()
    
    centrar_ventana(ventana_registrar_cita, 5, 3, 3)

    # Botón para revisar disponibilidad
    def revisar_disponibilidad():
        if combo_pacientes.get() and combo_doctores.get():
            doctor_seleccionado = combo_doctores.get()
            codigo_doctor = doctores_dict.get(doctor_seleccionado)  # Obtener el código del doctor
            paciente_seleccionado = combo_pacientes.get()
            codigo_paciente = pacientes_dic.get(paciente_seleccionado)
            abrir_ventana_calendario_citas(codigo_doctor, codigo_paciente)  # Obtener el código del paciente
        else:
            messagebox.showwarning("Advertencia", "Debe seleccionar un paciente y un doctor antes de continuar.")

    
    btn_revisar_disponibilidad = tk.Button(frame_registro, text="Revisar Disponibilidad", command=revisar_disponibilidad)
    btn_revisar_disponibilidad.pack(pady=20)

def abrir_ventana_calendario_citas(codigo_doctor, codigo_paciente):
    # Crear la ventana principal
    global ventana_calendario
    ventana_calendario = tk.Tk()
    ventana_calendario.title('Registrar cita')
    centrar_ventana(ventana_calendario, 5, 3, 2)
    cargar_logo(ventana_calendario)


    # Calendario
    cal = Calendar(ventana_calendario, selectmode='day', year=2024, month=11, day=20)
    cal.pack(pady=20)

    # Reloj (hora)
    hour_label = tk.Label(ventana_calendario, text="Hora:")
    hour_label.pack(pady=5)

    # Combobox para seleccionar la hora (en formato 1:00, 2:00, ..., 12:00)
    hour_combobox = ttk.Combobox(ventana_calendario, values=[f"{i}:00 - {i + 1}:00" for i in range(9, 21)], width=12)
    hour_combobox.set("9:00 - 10:00")  # valor por defecto
    hour_combobox.pack(pady=20)

    # Botón para agendar cita
    tk.Button(ventana_calendario, text='Agendar Cita', command=lambda: obtener_cita(cal, hour_combobox, codigo_doctor, codigo_paciente)).pack(pady=20)

    # Etiqueta para mostrar la cita agendada
    appointment_label = tk.Label(ventana_calendario, text="", font=("Helvetica", 12))
    appointment_label.pack(pady=20)

def abrir_ventana_editar_cita():
    # Crear una ventana para seleccionar la cita a editar
    global ventana_editar_cita
    ventana_editar_cita = tk.Toplevel()
    ventana_editar_cita.title("Editar Cita")
    frame_editar = tk.Frame(ventana_editar_cita)
    frame_editar.pack(padx=10, pady=10)
    cargar_logo(ventana_editar_cita)
    centrar_ventana(ventana_editar_cita, 7, 7, 3)

    # Conectar y obtener los códigos de citas existentes
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM citas")
            citas = cursor.fetchall()
            lista_citas = [str(cita[0]) for cita in citas]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos de las citas: {e}")
        return

    # Mostrar la lista de citas
    tk.Label(frame_editar, text="Seleccione el ID de la cita a editar:").pack(pady=5)
    combo_citas = ttk.Combobox(frame_editar, values=lista_citas)
    combo_citas.pack()

    # Botón para continuar con la edición
    tk.Button(frame_editar, text="Continuar", command=lambda: continuar_edicion_cita(combo_citas.get())).pack(pady=20)

def continuar_edicion_cita(codigo_cita):
    if not codigo_cita:
        messagebox.showwarning("Advertencia", "Debe seleccionar una cita.")
        return
    
    # Cerrar la ventana de selección de cita
    ventana_editar_cita.destroy()
    abrir_ventana_calendario_edicion(codigo_cita)

def abrir_ventana_calendario_edicion(codigo_cita):
    # Crear la ventana de edición de calendario
    global ventana_calendario_edicion
    ventana_calendario_edicion = tk.Toplevel()
    ventana_calendario_edicion.title('Editar Cita')
    cargar_logo(ventana_calendario_edicion)
    centrar_ventana(ventana_calendario_edicion, 5, 3, 2)

    # Calendario
    cal = Calendar(ventana_calendario_edicion, selectmode='day', year=2024, month=11, day=20)
    cal.pack(pady=20)

    # Combobox para seleccionar la hora
    hour_combobox = ttk.Combobox(ventana_calendario_edicion, values=[f"{i}:00 - {i + 1}:00" for i in range(9, 21)], width=12)
    hour_combobox.set("9:00 - 10:00")  # Valor por defecto
    hour_combobox.pack(pady=20)

    # Botón para confirmar la edición
    tk.Button(ventana_calendario_edicion, text='Confirmar Edición', command=lambda: confirmar_edicion_cita(cal, hour_combobox, codigo_cita)).pack(pady=20)

def confirmar_edicion_cita(calendario, caja_horas, codigo_cita):
    fecha_seleccionada = calendario.selection_get()
    hora = caja_horas.get()
    hora_inicial = hora.split(' - ')[0]  # Extraer "9:00" de "9:00 - 10:00"
    hora_seleccionada = f"{hora_inicial}:00"

    sabado_o_domingo = fecha_seleccionada.weekday() in (5, 6)

    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            # Verificar si hay una cita existente en esa fecha/hora para otro paciente
            cursor.execute(f"SELECT codigo_doctor FROM citas WHERE codigo = {codigo_cita}")
            resultado = cursor.fetchone()
            codigo_doctor = resultado[0] if resultado else ""
            
            cursor.execute(f"SELECT * FROM citas WHERE fecha = '{fecha_seleccionada}' AND hora = '{hora_seleccionada}' AND codigo_doctor = {codigo_doctor}")
            citas_existentes = cursor.fetchall()

            if citas_existentes or sabado_o_domingo:
                messagebox.showerror("No Disponible", "El doctor no está disponible en esa fecha y hora.")
            else:
                # Confirmar actualización
                confirmacion = messagebox.askyesno(
                    "Confirmar Edición",
                    f"¿Deseas actualizar la cita con código {codigo_cita} a la nueva fecha {fecha_seleccionada} y hora {hora_seleccionada}?"
                )
                if confirmacion:
                    cursor.execute(
                        f"UPDATE citas SET fecha = '{fecha_seleccionada}', hora = '{hora_seleccionada}' WHERE codigo = {codigo_cita}"
                    )
                    connection.commit()
                    messagebox.showinfo("Cita Actualizada", "La cita ha sido actualizada exitosamente.")
                    ventana_calendario_edicion.destroy()
                    ventana_citas_empleados.lift()
                    refresh_table(tablaCitasEmpleados, "citas")

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo editar la cita: {e}")
        print(e)

def obtener_cita(calendario, caja_horas, codigo_doctor, codigo_paciente):
    # Obtener la fecha seleccionada en el calendario
    fecha_seleccionada = calendario.selection_get()

    hora = caja_horas.get()  # Esto devuelve "9:00 - 10:00" como string
    
    # Extraer la primera parte de la hora (antes del guion)
    hora_inicial = hora.split(' - ')[0]  # Obtiene "9:00" de "9:00 - 10:00"
    hora_seleccionada = f"{hora_inicial}:00"  # Formatear correctamente la hora
    
    sabado_o_domingo = fecha_seleccionada.weekday() in (5, 6)



    try:
        connection, cursor = conectar_db()
        
        if connection and cursor:
            cursor.execute(f"SELECT * FROM citas WHERE fecha = '{fecha_seleccionada}' AND hora = '{hora_seleccionada}' AND codigo_doctor = {codigo_doctor}")
            citas_existentes = cursor.fetchall()
            
            if citas_existentes or sabado_o_domingo:
                messagebox.showerror("No Disponible", "El doctor no está disponible en esa fecha y hora.")
            else:
                cursor.execute(f"SELECT nombre FROM pacientes WHERE codigo = {codigo_paciente}")
                nombre_paciente = cursor.fetchone()
                
                cursor.execute(f"SELECT nombre FROM doctores WHERE codigo = {codigo_doctor}")
                nombre_doctor = cursor.fetchone()
                
                confirmacion = messagebox.askyesno(
                    "Confirmar Cita",
                    f"La cita está disponible. ¿Deseas agendar la cita para el paciente {nombre_paciente} con el doctor {nombre_doctor} el día {fecha_seleccionada} a las {hora_seleccionada}?"
                )
                if confirmacion:
                    # Código para registrar la cita en la base de datos
                    cursor.execute(
                        f"""
                        INSERT INTO citas (codigo_paciente, codigo_doctor, fecha, hora)
                        VALUES ({codigo_paciente}, {codigo_doctor}, '{fecha_seleccionada}', '{hora_seleccionada}')
                        """
                    )
                    connection.commit()
                    messagebox.showinfo("Cita Registrada", "La cita ha sido agendada exitosamente.")
                    
                else:
                    ventana_citas_empleados.lift()
                    ventana_registrar_cita.lift()
                    ventana_calendario.lift()
                    
                
            cursor.close()
            connection.close()
            
            ventana_calendario.destroy()
            ventana_registrar_cita.destroy()
            ventana_citas_empleados.lift()
            refresh_table(tablaCitasEmpleados, "citas")
        
            
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo verificar la disponibilidad: {e}")
        print(e)

def abrir_ventana_eliminar_cita():
    # Crear una ventana para seleccionar la cita a eliminar
    global ventana_eliminar_cita
    ventana_eliminar_cita = tk.Toplevel()
    ventana_eliminar_cita.title("Eliminar Cita")
    frame_editar = tk.Frame(ventana_eliminar_cita)
    frame_editar.pack(padx=10, pady=10)
    cargar_logo(ventana_eliminar_cita)
    centrar_ventana(ventana_eliminar_cita, 7, 7, 3)

    # Conectar y obtener los códigos de citas existentes
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM citas")
            citas = cursor.fetchall()
            lista_citas = [str(cita[0]) for cita in citas]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos de las citas: {e}")
        return

    # Mostrar la lista de citas
    tk.Label(frame_editar, text="Seleccione el ID de la cita a eliminar:").pack(pady=5)
    combo_citas = ttk.Combobox(frame_editar, values=lista_citas)
    combo_citas.pack()

    # Botón para continuar con la edición
    tk.Button(frame_editar, text="Continuar", command=lambda: continuar_eliminacion_cita(combo_citas.get())).pack(pady=20)

    def continuar_eliminacion_cita(codigo_cita):
        if not codigo_cita:
            messagebox.showwarning("Advertencia", "Debe seleccionar una cita.")
            return
        
        try:
            connection, cursor = conectar_db()
            if connection and cursor:

                confirmacion = messagebox.askyesno(
                    "Confirmar Edición",
                    f"¿Deseas eliminar la cita {codigo_cita}?"
                )
            if confirmacion:
                cursor.execute(f"DELETE FROM citas WHERE codigo = {codigo_cita};")
                connection.commit()
                messagebox.showinfo("Cita Eliminada", "La cita ha sido eliminada exitosamente.")
                ventana_citas_empleados.lift()
                refresh_table(tablaCitasEmpleados, "citas")
                

                cursor.close()
                connection.close()

            else:
                raise Exception("No se pudo conectar a la base de datos")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"No se pudo cargar los datos de las citas")
            return

def abrir_ventana_citas_doctores():
    global ventana_citas_doctores
    ventana_citas_doctores = tk.Toplevel()
    ventana_citas_doctores.title("Citas")
    cargar_logo(ventana_citas_doctores)
    
    frame_principal = tk.Frame(ventana_citas_doctores)
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
    global tabla_citas_doctores
    tabla_citas_doctores = ttk.Treeview(tree_frame, columns=("codigo", "paciente", "doctor", "fecha", "hora"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tabla_citas_doctores.pack(fill="both", expand=True)
    
    # Configuración de las columnas
    tabla_citas_doctores.heading("codigo", text="Código de cita")
    tabla_citas_doctores.heading("paciente", text="Paciente")
    tabla_citas_doctores.heading("doctor", text="Doctor")
    tabla_citas_doctores.heading("fecha", text="Fecha")
    tabla_citas_doctores.heading("hora", text="Hora")
    
    # Ajustar el tamaño de las columnas
    tabla_citas_doctores.column("codigo", width=50)
    tabla_citas_doctores.column("paciente", width=150)
    tabla_citas_doctores.column("doctor", width=150)
    tabla_citas_doctores.column("fecha", width=80)
    tabla_citas_doctores.column("hora", width=80)
    
    # Asignar los scrollbars al Treeview
    scrollbar_y.config(command=tabla_citas_doctores.yview)
    scrollbar_x.config(command=tabla_citas_doctores.xview)
    
    # Botones para registrar, editar y eliminar empleados
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Asignar consulta", width=15, command=asignar_consulta)
    btn_registrar.pack(side="left", padx=10)
    
    #btn_editar = tk.Button(button_frame, text="Editar", width=15, command=abrir_ventana_editar_cita)
    #btn_editar.pack(side="left", padx=10)
    
    #btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15)
    #btn_eliminar.pack(side="left", padx=10)
    
    
    btn_refresh = tk.Button(button_frame, text="Refresh", width=15, command=lambda: refresh_table(tabla_citas_doctores, "citas", user_id))
    btn_refresh.pack(side="right", padx=10)
    
    
    # Conectar y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute(f"SELECT citas.codigo, pacientes.nombre, doctores.nombre, citas.fecha, citas.hora FROM citas INNER JOIN pacientes ON citas.codigo_paciente = pacientes.codigo INNER JOIN doctores ON citas.codigo_doctor = doctores.codigo WHERE citas.codigo_doctor = {user_id} ORDER BY codigo ASC;")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tabla_citas_doctores.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_citas_doctores, 2, 2, 3)

def abrir_ventana_medicamentos():
    global ventana_medicamentos
    ventana_medicamentos = tk.Toplevel()
    ventana_medicamentos.title("Medicamentos")
    cargar_logo(ventana_medicamentos)
    
    frame_principal = tk.Frame(ventana_medicamentos)
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
    global tabla_medicamentos
    tabla_medicamentos = ttk.Treeview(tree_frame, columns=("codigo", "nombre", "via_adm", "presentacion", "fecha_cad"), show="headings", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    tabla_medicamentos.pack(fill="both", expand=True)
    
    # Configuración de las columnas
    tabla_medicamentos.heading("codigo", text="Código")
    tabla_medicamentos.heading("nombre", text="Nombre")
    tabla_medicamentos.heading("via_adm", text="Via de administración")
    tabla_medicamentos.heading("presentacion", text="Presentación")
    tabla_medicamentos.heading("fecha_cad", text="Fecha de caducidad")
    
    # Ajustar el tamaño de las columnas
    tabla_medicamentos.column("codigo", width=50)
    tabla_medicamentos.column("nombre", width=200)
    tabla_medicamentos.column("via_adm", width=80)
    tabla_medicamentos.column("presentacion", width=80)
    tabla_medicamentos.column("fecha_cad", width=80)
    
    # Asignar los scrollbars al Treeview
    scrollbar_y.config(command=tabla_medicamentos.yview)
    scrollbar_x.config(command=tabla_medicamentos.xview)
    
    # Botones para registrar, editar y eliminar empleados
    button_frame = tk.Frame(frame_principal)
    button_frame.pack(fill="x", pady=10)
    
    btn_registrar = tk.Button(button_frame, text="Registrar", width=15, command=registrar_medicamento)
    btn_registrar.pack(side="left", padx=10)
    
    btn_editar = tk.Button(button_frame, text="Editar", width=15, command=editar_medicamento)
    btn_editar.pack(side="left", padx=10)
    
    btn_eliminar = tk.Button(button_frame, text="Eliminar", width=15, command=eliminar_medicamento)
    btn_eliminar.pack(side="left", padx=10)
    
    
    btn_refresh = tk.Button(button_frame, text="Refresh", width=15, command=lambda: refresh_table(tabla_medicamentos, "medicamentos"))
    btn_refresh.pack(side="right", padx=10)
    
    
    # Conectar y mostrar los datos en la tabla
    connection, cursor = conectar_db()
    if connection and cursor:
        cursor.execute("SELECT * FROM medicamentos ORDER BY codigo ASC")  # Asegúrate de que la tabla existe y tiene estos campos
        rows = cursor.fetchall()
        for row in rows:
            tabla_medicamentos.insert("", "end", values=row)
        
        cursor.close()
        connection.close()
    
    centrar_ventana(ventana_medicamentos, 2, 2, 3)

def registrar_medicamento():
    # Ventana para registrar nuevo empleado
    ventana_registro_medicamento = tk.Toplevel()
    ventana_registro_medicamento.title("Registrar nuevo medicamento")
    cargar_logo(ventana_registro_medicamento)
    
    frame_registro = tk.Frame(ventana_registro_medicamento)
    frame_registro.pack(padx=10, pady=10)

    # Campos para registrar empleado
    labels = ["Nombre", "Via de administración", "Presentación", "Fecha de caducidad (YYYY-MM-DD)"]
    entries = []

    for label_text in labels:
        label = tk.Label(frame_registro, text=label_text)
        label.pack(pady=2)
        entry = tk.Entry(frame_registro)
        entry.pack(pady=2)
        entries.append(entry)

    def guardar_medicamento():
        # Recuperar los valores de los campos
        valores = [entry.get() for entry in entries]
        if all(valores):
            try:
                connection, cursor = conectar_db()
                if connection and cursor:
                    query = """
                        INSERT INTO medicamentos (nombre, via_adm, presentacion, fecha_cad)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query, tuple(valores))
                    connection.commit()
                    messagebox.showinfo("Éxito", "Medicamento registrado exitosamente")
                    cursor.close()
                    connection.close()
                    ventana_registro_medicamento.destroy()  # Cerrar la ventana de registro después de guardar
                    ventana_medicamentos.lift()
                else:
                    messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                    ventana_registro_medicamento.destroy()
                    ventana_medicamentos.lift()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el medicamento: {e}")
                ventana_registro_medicamento.lift()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            ventana_registro_medicamento.lift()

        refresh_table(tabla_medicamentos, "medicamentos")
    
    # Botón para guardar doctor
    btn_guardar = tk.Button(frame_registro, text="Guardar", command=guardar_medicamento)
    btn_guardar.pack(pady=10, side="left")
    btn_cancelar = tk.Button(frame_registro, text="Cancelar", command=lambda: cancelar(ventana_registro_medicamento, ventana_medicamentos))
    btn_cancelar.pack(pady=10, side="right")
    
    centrar_ventana(ventana_registro_medicamento, 4, 2, 3)

def editar_medicamento():
    # Ventana para registrar nuevo empleado

    ventana_editar_medicamento = tk.Toplevel()
    ventana_editar_medicamento.title("Editar Medicamento")
    frame_editar = tk.Frame(ventana_editar_medicamento)
    frame_editar.pack(padx=10, pady=10)
    cargar_logo(ventana_editar_medicamento)
    centrar_ventana(ventana_editar_medicamento, 7, 7, 3)

    # Conectar y obtener los códigos de citas existentes
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM medicamentos ORDER BY codigo ASC")
            medicamentos = cursor.fetchall()
            lista_medicamentos = [str(medicamento[0]) for medicamento in medicamentos]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"No se pudo cargar los datos de los medicamentos")
        return

    # Mostrar la lista de citas
    tk.Label(frame_editar, text="Seleccione el ID del medicamento a editar:").pack(pady=5)
    combo_medicamentos = ttk.Combobox(frame_editar, values=medicamentos)
    combo_medicamentos.pack()

    # Botón para continuar con la edición
    tk.Button(frame_editar, text="Continuar", command=lambda: continuar_edicion_medicamento(combo_medicamentos.get())).pack(pady=20)

    def continuar_edicion_medicamento(codigo_medicamento):
        ventana_editar_medicamento.destroy()
        ventana_edicion = tk.Toplevel()
        ventana_edicion.title("Editar información del medicamento")
        cargar_logo(ventana_edicion)
        centrar_ventana(ventana_edicion, 3, 2, 2)
    
        frame_edicion = tk.Frame(ventana_edicion)
        frame_edicion.pack(padx=10, pady=10)

        labels = ["Nombre", "Via de administración", "Presentación", "Fecha de caducidad (YYYY-MM-DD)"]
        entries = []

        try:
            connection, cursor = conectar_db()
            if connection and cursor:
                cursor.execute("SELECT nombre, via_adm, presentacion, fecha_cad FROM medicamentos WHERE codigo = %s", (codigo_medicamento,))
                medicamento = cursor.fetchone()
            
                if medicamento:
                    # Rellenar las entradas con la información actual
                    for i, label_text in enumerate(labels):
                        label = tk.Label(frame_edicion, text=label_text)
                        label.pack(pady=2)

                        entry = tk.Entry(frame_edicion)
                        entry.pack(pady=2)

                        # Establecer valor inicial desde la base de datos
                        entry.insert(0, str(medicamento[i]))
                        entries.append(entry)
                else:
                    messagebox.showerror("Error", "No se encontró al medicamento")
                    ventana_edicion.destroy()
                    return
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                ventana_edicion.destroy()
                return
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "Ocurrió un error al obtener la información del medicamento")
            ventana_edicion.destroy()
            return

        def guardar_medicamento():
            # Recuperar los valores de los campos
            valores = [entry.get() for entry in entries]
            if all(valores):
                try:
                    connection, cursor = conectar_db()
                    if connection and cursor:

                        confirmacion = messagebox.askyesno(
                        "Confirmar Edición",
                        f"¿Deseas actualizar la información del medicamento con código {codigo_medicamento}?"
                        )
                        if confirmacion:

                            sql_update = """
                            UPDATE medicamentos
                            SET nombre = %s, via_adm = %s, presentacion = %s, fecha_cad = %s
                            WHERE codigo = %s
                            """
                            cursor.execute(sql_update, (*valores, codigo_medicamento))

                            connection.commit()
                            messagebox.showinfo("Medicamento Actualizado", "La información del medicamento ha sido actualizada exitosamente.")
                            ventana_edicion.destroy()
                            ventana_medicamentos.lift()
                            refresh_table(tabla_medicamentos, "medicamentos")

                    else:
                        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                        ventana_edicion.destroy()
                        ventana_medicamentos.lift()
                except Exception as e:
                    print(e)
                    messagebox.showerror("Error", f"No se pudo editar la información del medicamento")
                    ventana_edicion.lift()
                
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                ventana_edicion.lift()
            
        refresh_table(tabla_medicamentos, "medicamentos")
        # Botón para guardar doctor
        btn_guardar = tk.Button(frame_edicion, text="Guardar", command=guardar_medicamento)
        btn_guardar.pack(pady=10, side="left")
        btn_cancelar = tk.Button(frame_edicion, text="Cancelar", command=lambda: cancelar(ventana_edicion, ventana_medicamentos))
        btn_cancelar.pack(pady=10, side="right")

def eliminar_medicamento():
    # Crear una ventana para seleccionar la cita a editar
    ventana_eliminar_medicamento = tk.Toplevel()
    ventana_eliminar_medicamento.title("Eliminar Medicamento")
    frame_eliminar = tk.Frame(ventana_eliminar_medicamento)
    frame_eliminar.pack(padx=10, pady=10)
    cargar_logo(ventana_eliminar_medicamento)
    centrar_ventana(ventana_eliminar_medicamento, 7, 7, 3)

    # Conectar y obtener los códigos de citas existentes
    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute("SELECT codigo FROM medicamentos ORDER BY codigo ASC;")
            medicamentos = cursor.fetchall()
            lista_medicamentos = [str(medicamento[0]) for medicamento in medicamentos]  # Convertir los códigos a string

            cursor.close()
            connection.close()
        else:
            raise Exception("No se pudo conectar a la base de datos")
    except Exception as e:
        print(e)
        messagebox.showerror("Error", f"No se pudo cargar los datos de los medicamentos")
        return

    # Mostrar la lista de citas
    tk.Label(frame_eliminar, text="Seleccione el ID del medicamento a eliminar:").pack(pady=5)
    combo_medicamentos = ttk.Combobox(frame_eliminar, values=lista_medicamentos)
    combo_medicamentos.pack()

    # Botón para continuar con la edición
    tk.Button(frame_eliminar, text="Continuar", command=lambda: continuar_eliminacion_medicamento(combo_medicamentos.get())).pack(pady=20)

    def continuar_eliminacion_medicamento(codigo_medicamento):
        if not codigo_medicamento:
            messagebox.showwarning("Advertencia", "Debe seleccionar un codigo de medicamento.")
            return
        
        try:
            connection, cursor = conectar_db()
            if connection and cursor:

                confirmacion = messagebox.askyesno(
                    "Confirmar Eliminacion",
                    f"¿Deseas eliminar al medicamento {codigo_medicamento}?"
                )
                if confirmacion:
                    cursor.execute(f"DELETE FROM medicamentos WHERE codigo = {codigo_medicamento};")
                    connection.commit()
                    messagebox.showinfo("Medicamento Eliminado", "El medicamento ha sido eliminado exitosamente.")
                    ventana_medicamentos.lift()
                    refresh_table(tabla_medicamentos, "medicamentos")
                
                    cursor.close()
                    connection.close()

            else:
                raise Exception("No se pudo conectar a la base de datos")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"No se pudo cargar los datos de los medicamentos")
            return
        
        
def cerrar_sesion():
    ventana_menu.destroy()
    login()

login()
