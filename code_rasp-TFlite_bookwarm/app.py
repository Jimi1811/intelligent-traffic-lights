############################################################
######################## importar librerias ################
############################################################

from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from picamera import PiCamera
import base64
import io

from detection import load_model, load_labels, process_image, display_result 
from detection import Poco_trafico, Mucho_trafico, traffic_light_sequence

############################################################
######################## inicializacion ####################
############################################################

app = Flask(__name__)
socketio = SocketIO(app)
camera = PiCamera()

############################################################
######################## definir rutas de la app ###########
############################################################

### ruta para la plantilla principal
@app.route('/')
def index():
    return render_template('index.html')

### conectar al cliente
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado.')



### generar el stream (envio de fotogramas)
def generate_stream():
    while True:
        # Capturar un fotograma desde el módulo de cámara
        frame = io.BytesIO()
        camera.capture(frame, format='jpeg')
        frame.seek(0)

        # Convertir el fotograma a base64
        frame_data = base64.b64encode(frame.read()).decode('utf-8')
        frame.seek(0)

        # Realizar la detección de objetos
        image = preprocess_image(frame_data)  # Implementa la función según las necesidades de tu modelo
        detections = run_inference(image)

        # Enviar el fotograma a través de WebSockets
        socketio.emit('livestream', {'frame': frame_data, 'detections': detections})

### ruta para la recepcion del video
@app.route('/video_feed')
def video_feed():
    return Response(generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
