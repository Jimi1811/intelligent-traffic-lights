# Importar la libreria Flask
# render_template: renderizar archivos en html 
# request, flash, redirect, url_for -> para agregar usuario
from flask import Flask, render_template, request,flash, redirect, url_for, session

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

# Crear ruta principal
@app.route('/service')
 # Crear inicio
def service():
    # Corra un texto
    return render_template('service.html')

# Ruta para error
# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('error.html')

# Crear funcion
if __name__ == '__main__':
    # Correr programa, hacer debug true, especificar puerto (default: 5000)
    app.run(port=5000,debug=True)