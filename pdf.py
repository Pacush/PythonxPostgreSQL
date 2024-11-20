import os

import jinja2
import pdfkit
import psycopg2


def conectar_db():
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='12345',
            database='NucleoDeDiagnostico',
            port ='5433'    #Cambiar dependiendo del puerto asignado en tu servidor
        )
        
        cursor = connection.cursor()
        return connection, cursor
    except Exception as ex:
        print(f"Error al conectar a la base de datos: {ex}")
        return None, None

def consulta2pdf(codigo_cita, diagnostico, codigo_medicamento):

    ruta_absoluta = os.path.abspath("logo2.png")

    options = {
        'enable-local-file-access': None,
        'enable-javascript': None
    }

    try:
        connection, cursor = conectar_db()
        if connection and cursor:
            cursor.execute(f"SELECT codigo_paciente FROM citas WHERE codigo = {codigo_cita}")
            codigo_paciente = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT doctores.nombre FROM citas INNER JOIN doctores ON citas.codigo_doctor = doctores.codigo WHERE citas.codigo = {codigo_cita};")
            nombre_doctor = cursor.fetchone()

            cursor.execute(f"SELECT * FROM pacientes WHERE codigo = {codigo_paciente};")
            paciente = cursor.fetchall()
            
            cursor.execute(f"SELECT * FROM medicamentos WHERE codigo = {codigo_medicamento};")
            medicamento = cursor.fetchall()
            
            cursor.close()
            connection.close()

        else:
            print(f"No se pudo imprimir la consulta: {e}")
            return False
    except Exception as e:
        print(f"No se pudo imprimir la consulta: {e}")
        return False
    
    
    nombre_paciente = paciente[0][1]
    direccion_paciente = paciente[0][2]
    telefono_paciente = paciente[0][3]
    sexo_paciente = paciente[0][5]
    edad_paciente = paciente[0][6]
    estatura_paciente = paciente[0][7]
    
    nombre_medicamento = medicamento[0][1]
    via_adm_medicamento = medicamento[0][2]
    presentacion_medicamento = medicamento[0][3]
    fecha_cad_medicamento = medicamento[0][4]
    
    nombre_doctor = nombre_doctor[0]


    nombre_archivo = f"./Recetas de consultas/receta.pdf"

    context = {'ruta_logo': ruta_absoluta, 'nombre_paciente': nombre_paciente, 'edad_paciente': edad_paciente,
            'estatura_paciente': estatura_paciente, 'sexo_paciente': sexo_paciente,
            'direccion_paciente': direccion_paciente, 'telefono_paciente': telefono_paciente,
            'diagnostico': diagnostico,'nombre_medicamento': nombre_medicamento,
            'via_adm_medicamento': via_adm_medicamento, 'presentacion_medicamento': presentacion_medicamento,
            'fecha_cad_medicamento': fecha_cad_medicamento, 'nombre_doctor': nombre_doctor}

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template("receta_html2pdf.html")
    output_text = template.render(context)
    path= r"wkhtmltopdf\bin\wkhtmltopdf.exe"

    config = pdfkit.configuration(wkhtmltopdf=path)

    pdfkit.from_string(output_text, nombre_archivo, configuration=config, options=options)
    
    return True

