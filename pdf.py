import os

import jinja2
import pdfkit

ruta_absoluta = os.path.abspath("logo2.png")

options = {
    'enable-local-file-access': None,
    'enable-javascript': None
}

# Valores de prueba. Estos deben ser obtenidos desde la consulta
nombre_paciente = "José"
edad_paciente = 20
estatura_paciente = 1.70
sexo_paciente = "MASCULINO"
direccion_paciente = "NAPOLES 95"
telefono_paciente = "3331563135"

diagnostico = "Hola, esto es una prueba."

nombre_medicamento = "Paracetamol"
via_adm_medicamento = "Oral"
presentacion_medicamento = "Tableta"
fecha_cad_medicamento = "2025-05-05"
nombre_doctor = "Josue Lugo"

nombre_archivo = f"./Recetas de consultas/consulta_{nombre_paciente}.pdf"

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