import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from PIL import Image, ImageTk


# Configuración de la conexión a la base de datos
DB_HOST = "localhost"
DB_NAME = "dbjuan"
DB_USER = "admin"
DB_PASS = "admin"

# Conexión a la base de datos
def connect_db():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)



# Definición de la clase Nodo
class Nodo:
    def __init__(self, value):
        self.value = value
        self.next = None

# Definición de la clase Lista
class Lista:
    def __init__(self):
        self.head = None
        self.tail = None

    def agregar_dato_inicio(self, value):
        nodo = Nodo(value)
        if self.head is None:
            self.head = self.tail = nodo
        else:
            nodo.next = self.head
            self.head = nodo

    def eliminar_dato_inicio(self):
        if self.head is None:
            return
        self.head = self.head.next

    def print_lista(self):
        if self.head is None:
            return "Tu lista está vacía"
        valores = []
        temp = self.head
        while temp is not None:
            valores.append(temp.value)
            temp = temp.next
        return valores

# Datos de ejemplo para la tabla de empleados
empleados = []

def login():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    if usuario == "admin" and contraseña == "1234":
        ventana_login.destroy()  # Cierra la ventana de login
        pagina_tabla_empleados()  # Muestra la tabla de empleados
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def pagina_principal():
    ventana_tabla = tk.Tk()
    ventana_tabla.title("Tabla de Empleados")




    # Crear la tabla
    tree = ttk.Treeview(ventana_tabla, columns=("ID", "Nombre", "Apellido", "NSS", "Fecha_Nac", 
                                                  "Direccion", "Ciudad", "Sexo", "Salario", 
                                                  "NSS_sup", "N_dep"), show='headings')
    # Definir las cabeceras
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre principal")
    tree.heading("Apellido", text="Apellido")
    tree.heading("NSS", text="NSS")
    tree.heading("Fecha_Nac", text="Fecha de nacimiento")
    tree.heading("Direccion", text="Dirección")
    tree.heading("Ciudad", text="Ciudad")
    tree.heading("Sexo", text="Sexo")
    tree.heading("Salario", text="Salario")
    tree.heading("NSS_sup", text="NSS del supervisor")
    tree.heading("N_dep", text="Número de departamento")

    tree.pack(pady=5)

    # Funciones para manejar el agregado, edición y eliminación
    def agregar_empleado():
        empleado = {
            "ID": entry_id.get(),
            "Nombre": entry_nombre.get(),
            "Apellido": entry_apellido.get(),
            "NSS": entry_nss.get(),
            "Fecha_Nac": entry_fecha_nac.get(),
            "Direccion": entry_direccion.get(),
            "Ciudad": entry_ciudad.get(),
            "Sexo": entry_sexo.get(),
            "Salario": entry_salario.get(),
            "NSS_sup": entry_nss_sup.get(),
            "N_dep": entry_n_dep.get()
        }

        if not all(empleado.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        empleados.append(empleado)
        actualizar_tabla()
        limpiar_campos()

    def editar_empleado():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un empleado para editar.")
            return
        
        empleado = {
            "ID": entry_id.get(),
            "Nombre": entry_nombre.get(),
            "Apellido": entry_apellido.get(),
            "NSS": entry_nss.get(),
            "Fecha_Nac": entry_fecha_nac.get(),
            "Direccion": entry_direccion.get(),
            "Ciudad": entry_ciudad.get(),
            "Sexo": entry_sexo.get(),
            "Salario": entry_salario.get(),
            "NSS_sup": entry_nss_sup.get(),
            "N_dep": entry_n_dep.get()
        }

        if not all(empleado.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        empleado_index = tree.index(selected_item)
        empleados[empleado_index] = empleado
        actualizar_tabla()
        limpiar_campos()

    def eliminar_empleado():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un empleado para eliminar.")
            return
        
        empleado_index = tree.index(selected_item)
        empleados.pop(empleado_index)
        actualizar_tabla()

    def actualizar_tabla():
        for row in tree.get_children():
            tree.delete(row)
        for empleado in empleados:
            tree.insert("", tk.END, values=(empleado["ID"], empleado["Nombre"], empleado["Apellido"],
                                             empleado["NSS"], empleado["Fecha_Nac"], empleado["Direccion"],
                                             empleado["Ciudad"], empleado["Sexo"], empleado["Salario"],
                                             empleado["NSS_sup"], empleado["N_dep"]))

    def limpiar_campos():
        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_nss.delete(0, tk.END)
        entry_fecha_nac.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_ciudad.delete(0, tk.END)
        entry_sexo.delete(0, tk.END)
        entry_salario.delete(0, tk.END)
        entry_nss_sup.delete(0, tk.END)
        entry_n_dep.delete(0, tk.END)

    # Entradas para agregar/editar empleados
    tk.Label(ventana_tabla, text="ID:").pack()
    entry_id = tk.Entry(ventana_tabla)
    entry_id.pack()

    tk.Label(ventana_tabla, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_tabla)
    entry_nombre.pack()

    tk.Label(ventana_tabla, text="Apellido:").pack()
    entry_apellido = tk.Entry(ventana_tabla)
    entry_apellido.pack()

    tk.Label(ventana_tabla, text="NSS:").pack()
    entry_nss = tk.Entry(ventana_tabla)
    entry_nss.pack()

    tk.Label(ventana_tabla, text="Fecha de Nacimiento:").pack()
    entry_fecha_nac = tk.Entry(ventana_tabla)
    entry_fecha_nac.pack()

    tk.Label(ventana_tabla, text="Dirección:").pack()
    entry_direccion = tk.Entry(ventana_tabla)
    entry_direccion.pack()

    tk.Label(ventana_tabla, text="Ciudad:").pack()
    entry_ciudad = tk.Entry(ventana_tabla)
    entry_ciudad.pack()

    tk.Label(ventana_tabla, text="Sexo:").pack()
    entry_sexo = tk.Entry(ventana_tabla)
    entry_sexo.pack()

    tk.Label(ventana_tabla, text="Salario:").pack()
    entry_salario = tk.Entry(ventana_tabla)
    entry_salario.pack()

    tk.Label(ventana_tabla, text="NSS del Supervisor:").pack()
    entry_nss_sup = tk.Entry(ventana_tabla)
    entry_nss_sup.pack()

    tk.Label(ventana_tabla, text="Número de Departamento:").pack()
    entry_n_dep = tk.Entry(ventana_tabla)
    entry_n_dep.pack()

    # Botones para agregar, editar y eliminar
    btn_agregar = tk.Button(ventana_tabla, text="Agregar", command=agregar_empleado)
    btn_agregar.pack(pady=5)

    btn_editar = tk.Button(ventana_tabla, text="Editar", command=editar_empleado)
    btn_editar.pack(pady=5)

    btn_eliminar = tk.Button(ventana_tabla, text="Eliminar", command=eliminar_empleado)
    btn_eliminar.pack(pady=5)

    # Inicializar la tabla
    actualizar_tabla()

    ventana_tabla.mainloop()


def pagina_tabla_empleados():
    ventana_tabla = tk.Tk()
    ventana_tabla.title("Tabla de Empleados")




    # Crear la tabla
    tree = ttk.Treeview(ventana_tabla, columns=("ID", "Nombre", "Apellido", "NSS", "Fecha_Nac", 
                                                  "Direccion", "Ciudad", "Sexo", "Salario", 
                                                  "NSS_sup", "N_dep"), show='headings')
    # Definir las cabeceras
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre principal")
    tree.heading("Apellido", text="Apellido")
    tree.heading("NSS", text="NSS")
    tree.heading("Fecha_Nac", text="Fecha de nacimiento")
    tree.heading("Direccion", text="Dirección")
    tree.heading("Ciudad", text="Ciudad")
    tree.heading("Sexo", text="Sexo")
    tree.heading("Salario", text="Salario")
    tree.heading("NSS_sup", text="NSS del supervisor")
    tree.heading("N_dep", text="Número de departamento")

    tree.pack(pady=5)

    # Funciones para manejar el agregado, edición y eliminación
    def agregar_empleado():
        empleado = {
            "ID": entry_id.get(),
            "Nombre": entry_nombre.get(),
            "Apellido": entry_apellido.get(),
            "NSS": entry_nss.get(),
            "Fecha_Nac": entry_fecha_nac.get(),
            "Direccion": entry_direccion.get(),
            "Ciudad": entry_ciudad.get(),
            "Sexo": entry_sexo.get(),
            "Salario": entry_salario.get(),
            "NSS_sup": entry_nss_sup.get(),
            "N_dep": entry_n_dep.get()
        }

        if not all(empleado.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        empleados.append(empleado)
        actualizar_tabla()
        limpiar_campos()

    def editar_empleado():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un empleado para editar.")
            return
        
        empleado = {
            "ID": entry_id.get(),
            "Nombre": entry_nombre.get(),
            "Apellido": entry_apellido.get(),
            "NSS": entry_nss.get(),
            "Fecha_Nac": entry_fecha_nac.get(),
            "Direccion": entry_direccion.get(),
            "Ciudad": entry_ciudad.get(),
            "Sexo": entry_sexo.get(),
            "Salario": entry_salario.get(),
            "NSS_sup": entry_nss_sup.get(),
            "N_dep": entry_n_dep.get()
        }

        if not all(empleado.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        empleado_index = tree.index(selected_item)
        empleados[empleado_index] = empleado
        actualizar_tabla()
        limpiar_campos()

    def eliminar_empleado():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un empleado para eliminar.")
            return
        
        empleado_index = tree.index(selected_item)
        empleados.pop(empleado_index)
        actualizar_tabla()

    def actualizar_tabla():
        for row in tree.get_children():
            tree.delete(row)
        for empleado in empleados:
            tree.insert("", tk.END, values=(empleado["ID"], empleado["Nombre"], empleado["Apellido"],
                                             empleado["NSS"], empleado["Fecha_Nac"], empleado["Direccion"],
                                             empleado["Ciudad"], empleado["Sexo"], empleado["Salario"],
                                             empleado["NSS_sup"], empleado["N_dep"]))

    def limpiar_campos():
        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_nss.delete(0, tk.END)
        entry_fecha_nac.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_ciudad.delete(0, tk.END)
        entry_sexo.delete(0, tk.END)
        entry_salario.delete(0, tk.END)
        entry_nss_sup.delete(0, tk.END)
        entry_n_dep.delete(0, tk.END)

    # Entradas para agregar/editar empleados
    tk.Label(ventana_tabla, text="ID:").pack()
    entry_id = tk.Entry(ventana_tabla)
    entry_id.pack()

    tk.Label(ventana_tabla, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_tabla)
    entry_nombre.pack()

    tk.Label(ventana_tabla, text="Apellido:").pack()
    entry_apellido = tk.Entry(ventana_tabla)
    entry_apellido.pack()

    tk.Label(ventana_tabla, text="NSS:").pack()
    entry_nss = tk.Entry(ventana_tabla)
    entry_nss.pack()

    tk.Label(ventana_tabla, text="Fecha de Nacimiento:").pack()
    entry_fecha_nac = tk.Entry(ventana_tabla)
    entry_fecha_nac.pack()

    tk.Label(ventana_tabla, text="Dirección:").pack()
    entry_direccion = tk.Entry(ventana_tabla)
    entry_direccion.pack()

    tk.Label(ventana_tabla, text="Ciudad:").pack()
    entry_ciudad = tk.Entry(ventana_tabla)
    entry_ciudad.pack()

    tk.Label(ventana_tabla, text="Sexo:").pack()
    entry_sexo = tk.Entry(ventana_tabla)
    entry_sexo.pack()

    tk.Label(ventana_tabla, text="Salario:").pack()
    entry_salario = tk.Entry(ventana_tabla)
    entry_salario.pack()

    tk.Label(ventana_tabla, text="NSS del Supervisor:").pack()
    entry_nss_sup = tk.Entry(ventana_tabla)
    entry_nss_sup.pack()

    tk.Label(ventana_tabla, text="Número de Departamento:").pack()
    entry_n_dep = tk.Entry(ventana_tabla)
    entry_n_dep.pack()

    # Botones para agregar, editar y eliminar
    btn_agregar = tk.Button(ventana_tabla, text="Agregar", command=agregar_empleado)
    btn_agregar.pack(pady=5)

    btn_editar = tk.Button(ventana_tabla, text="Editar", command=editar_empleado)
    btn_editar.pack(pady=5)

    btn_eliminar = tk.Button(ventana_tabla, text="Eliminar", command=eliminar_empleado)
    btn_eliminar.pack(pady=5)

    # Inicializar la tabla
    actualizar_tabla()

    ventana_tabla.mainloop()

# Crear la ventana de inicio de sesión
ventana_login = tk.Tk()
ventana_login.title("Inicio de Sesión")

tk.Label(ventana_login, text="Usuario:").pack(pady=5)
entry_usuario = tk.Entry(ventana_login)
entry_usuario.pack(pady=5)

tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
entry_contraseña = tk.Entry(ventana_login, show="*")
entry_contraseña.pack(pady=5)

btn_login = tk.Button(ventana_login, text="Iniciar Sesión", command=login)
btn_login.pack(pady=20)

ventana_login.mainloop()