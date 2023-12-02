# Importar la libreria Flask
# render_template: renderizar archivos en html 
# request, flash, redirect, url_for -> para agregar usuario
from flask import Flask, render_template, request,flash, redirect, url_for, session

# Importar la clase RecordingsDAO
from dao.DAOinter_rec import RecordingsDAO, IntersectionsDAO

# Crear instancias de las clases DAO
recordings_dao = RecordingsDAO()
intersections_dao = IntersectionsDAO()

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


@app.route('/menu')
def menu():
    # Obtener todas las grabaciones y todas las intersecciones
    recordings = recordings_dao.get_all_recordings()
    intersections = intersections_dao.get_all_intersections()

    return render_template('menu.html', recordings=recordings, intersections=intersections)

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
    app.run(host='0.0.0.0', port=4000, debug=True, threaded=True)