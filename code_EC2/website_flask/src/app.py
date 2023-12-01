# Importar la libreria Flask
# render_template: renderizar archivos en html 
# request, flash, redirect, url_for -> para agregar usuario
from flask import Flask, render_template, request,flash, redirect, url_for, session
from flask import Response
import requests

# Crear aplicacion
app = Flask(__name__, static_folder='static')

# Crear llave secreta - contrasena
app.secret_key = "mys3cr3tk3y"

# Crear ruta principal
@app.route('/')
 # Crear inicio
def inicio():
    # Corra un texto
    return render_template('index.html')

# Crear ruta principal
@app.route('/about')
 # Crear inicio
def about():
    # Corra un texto
    return render_template('about.html')


# Crear ruta principal
@app.route('/contact')
 # Crear inicio
def contact():
    # Corra un texto
    return render_template('contact.html')


# Crear ruta principal
@app.route('/menu')
 # Crear inicio
def menu():
    # Corra un texto
    return render_template('menu.html')

@app.route('/service')
def service():
    return render_template('service.html')

def generate():
    # Cambia la URL al enlace externo de tu stream mpegts
    video_url = "http://proxy18.rt3.io:38817"
    response = requests.get(video_url, stream=True)

    for chunk in response.iter_content(chunk_size=1024):
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + chunk + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Crear funcion
if __name__ == '__main__':
    # Correr programa, hacer debug true, especificar puerto (default: 5000)
    app.run(port=3000,debug=True)