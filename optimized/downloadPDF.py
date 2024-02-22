from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import fonts
from reportlab.lib.utils import simpleSplit
import os
import tempfile
import time


app = Flask(__name__)


# Abre index
@app.route('/')
def index():
    return render_template('index.html')


# Abre inspección
@app.route('/servicio', methods=['GET', 'POST'])
def servicio():
    return render_template('servicio.html')




# Genera pdf de inspección
@app.route('/pdfinspeccion', methods=['GET', 'POST'])
def submit():

    header = 'static/img/headerInspeccion.png'
    footer = 'static/img/footer.png'

    fecha_inspeccion = request.form.get('fecha_inspeccion')
    nombre_cliente = request.form['nombre_cliente']
    servicio_solicitado = request.form['servicio_solicitado']

    if servicio_solicitado == 'Mantenimiento' or servicio_solicitado == 'Reparación' or servicio_solicitado == 'Instalación':
        equipo_diagnosticado = request.form.get('equipo_diagnosticado', '')
    else:
        equipo_diagnosticado = None


    proveedor_asignado = request.form['proveedor_asignado']
    diagnostico = request.form['diagnostico']
    evidencias = request.files['evidencias']

    pdf_filename = ''


    pdf_filename = f"Inspección - {nombre_cliente}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    c.drawImage(header, 50, 670, width=500, height= 105) 

    c.setFont("Helvetica-Bold", 12)  
    c.drawString(100, 630, "Fecha de inspección: ")
    c.setFont("Helvetica", 12)  
    c.drawString(228, 630, fecha_inspeccion)  

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 600, "Cliente: ")
    c.setFont("Helvetica", 12)
    c.drawString(148, 600, nombre_cliente)  

    c.setFont("Helvetica-Bold", 12)
    c.drawString(370, 600, "Servicio: ")
    c.setFont("Helvetica", 12)
    c.drawString(424, 600, servicio_solicitado)  

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 570, "Proveedor: ")
    c.setFont("Helvetica", 12)
    c.drawString(168, 570, proveedor_asignado)  

    if equipo_diagnosticado != None:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(370, 570, "Equipo: ")
        c.setFont("Helvetica", 12)
        c.drawString(420, 570, equipo_diagnosticado)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 520, "Resumen de inspección: ")
    c.setFont("Helvetica", 12)

    left_margin = 100
    top_margin = 500  
    width, height = letter
    text_width = width - 2 * left_margin

    lines = simpleSplit(diagnostico, "Helvetica", 12, text_width)

    for line in lines:
        c.drawString(left_margin, top_margin, line)
        top_margin -= 14

    c.drawImage(footer, 50, 10, width=500, height=200) 

    if evidencias and 'evidencias' in request.files:

        evidencias = request.files.getlist('evidencias')

        # Determinar las dimensiones de la página
        page_width, page_height = letter
        margin_horizontal = 25
        margin_vertical = 75  # Aumentamos el margen vertical

        # Tamaño de las imágenes
        image_width = (page_width - 4 * margin_horizontal) / 3  # Tres imágenes por página con márgenes
        image_height = (page_height - 2 * margin_vertical - 95) / 1  # Altura ajustada para una sola fila de imágenes

        for i, file in enumerate(evidencias):
            # Comprobar si se necesita una nueva página
            if i % 3 == 0:  # Nueva página cada 3 imágenes
                c.showPage()
                c.drawImage(header, 50, 670, width=500, height=105) 
                c.setFont("Helvetica-Bold", 12)
                c.drawString(270, 630, "Evidencias")
                y = page_height - margin_vertical + 10 - image_height  # Posición inicial de y para las imágenes

            temp_directory = tempfile.gettempdir()
            image_path = os.path.join(temp_directory, file.filename)
            file.save(image_path)

            # Calcular la posición x para la imagen actual
            col = i % 3  # Columna actual (0, 1, 2)
            x = margin_horizontal + col * (image_width + margin_horizontal)

            # Dibujar la imagen actual en la posición calculada
            c.drawImage(image_path, x, y, width=image_width, height=image_height, preserveAspectRatio=True)
            os.remove(image_path)


        c.drawImage(footer, 50, 10, width=500, height=200)

        c.save()

        time.sleep(2)

    return redirect(url_for('index'))








# Genera pdf de servicio
@app.route('/pdfservicio', methods=['GET', 'POST'])
def submit_1():

    header = 'static/img/headerServicio.png'
    footer = 'static/img/footer.png'

    fecha_inspeccion = request.form.get('fecha_inspeccion')
    nombre_cliente = request.form['nombre_cliente']
    servicio_solicitado = request.form['servicio_solicitado']

    if servicio_solicitado == 'Mantenimiento' or servicio_solicitado == 'Reparación' or servicio_solicitado == 'Instalación':
        equipo_diagnosticado = request.form.get('equipo_diagnosticado', '')
    else:
        equipo_diagnosticado = None


    proveedor_asignado = request.form['proveedor_asignado']
    diagnostico = request.form['diagnostico']
    evidencias = request.files['evidencias']

    pdf_filename = ''


    pdf_filename = f" - {nombre_cliente}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    c.drawImage(header, 50, 670, width=500, height= 115) 

    c.drawString(100, 630, "Fecha de inspección: " +  fecha_inspeccion)  
    c.drawString(100, 600, "Cliente: " + nombre_cliente)  
    c.drawString(370, 600, "Servicio: " + servicio_solicitado)  
    c.drawString(100, 570, "Proveedor asignado: " + proveedor_asignado)  


    if equipo_diagnosticado != None: 
        c.drawString(370, 570, "Equipo: " + equipo_diagnosticado)


    c.drawString(100, 530, "Resumen de inspección: ") 

    left_margin = 100
    top_margin = 510  
    width, height = letter
    text_width = width - 2 * left_margin

    lines = simpleSplit(diagnostico, "Helvetica", 12, text_width)

    for line in lines:
        c.drawString(left_margin, top_margin, line)
        top_margin -= 14

    c.drawImage(footer, 50, 10, width=500, height=200) 

    if evidencias and 'evidencias' in request.files:

        evidencias = request.files.getlist('evidencias')

        # Determinar las dimensiones de la página
        page_width, page_height = letter
        margin_horizontal = 50
        margin_vertical = 75  # Aumentamos el margen vertical

        # Tamaño de las imágenes
        image_width = (page_width - 4 * margin_horizontal) / 3  # Tres imágenes por página con márgenes
        image_height = (page_height - 2 * margin_vertical - 95) / 1  # Altura ajustada para una sola fila de imágenes

        for i, file in enumerate(evidencias):
            # Comprobar si se necesita una nueva página
            if i % 3 == 0:  # Nueva página cada 3 imágenes
                c.showPage()
                c.drawImage(header, 50, 670, width=500, height=95) 
                c.drawString(270, 630, "Evidencias")
                y = page_height - margin_vertical - 95 - image_height  # Posición inicial de y para las imágenes

            temp_directory = tempfile.gettempdir()
            image_path = os.path.join(temp_directory, file.filename)
            file.save(image_path)

            # Calcular la posición x para la imagen actual
            col = i % 3  # Columna actual (0, 1, 2)
            x = margin_horizontal + col * (image_width + margin_horizontal)

            # Dibujar la imagen actual en la posición calculada
            c.drawImage(image_path, x, y, width=image_width, height=image_height, preserveAspectRatio=True)
            os.remove(image_path)

    # Añadir el footer después de la última página de imágenes
    c.drawImage(footer, 50, 10, width=500, height=200)

    c.save()

    time.sleep(2)

    return redirect(url_for('servicio'))






@app.route('/download_pdf')
def download_pdf():
    return send_file(pdf_filename, as_attachment=True) 

if __name__ == '__main__':
    app.run(debug=True, port=2700)

