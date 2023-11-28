import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2
import time
import RPi.GPIO as GPIO

from flask import Flask, render_template
from flask_socketio import SocketIO
import base64

from traffic_light import seteo_pines, sincronizar_LEDs, sincronizar_trafico
from traffic_light import red_led_pin_1, red_led_pin_2, green_led_pin_1, green_led_pin_2, yellow_led_pin_1, yellow_led_pin_2
from object_detector import load_labels, load_model, process_image, display_result, config_cam, calculo_fps
from object_detector import CAMERA_HEIGHT, CAMERA_WIDTH, FRAME_RATE

model_path = '/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm/efficientdet_lite0.tflite'
label_path = '/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm//labels.txt'

class camera:
    def __init__(self):
        pass

    def config(self):
        picam2 = config_cam()
        return picam2

    def get_model(self, model_path, label_path):
        interpreter = load_model(model_path)
        labels = load_labels(label_path)
        return interpreter, labels
    
    def get_input_details(self, interpreter):
        input_details = interpreter.get_input_details()
        return input_details
    
    def get_params(self, input_details):
        input_shape = input_details[0]['shape']
        height = input_shape[1]
        width = input_shape[2]
        input_index = input_details[0]['index']
        return height, width, input_index
    
    def modificar_img(self, im, width, height):
        im = cv2.flip(im, -1)
        image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        image = image.resize((width, height))
        return image

    def resultados(self, interpreter, image, input_index, im, labels):
        top_result = process_image(interpreter, image, input_index)
        display_result(top_result, im, labels)
        return top_result

# inicializar aplicacion
app = Flask(__name__)
socketio = SocketIO(app)

# definir rutas
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    ## Inicializar variables
    fps = 0; vehicle_count = 0
    last_time = time.time() 

    ## Inicializar instancias
    cam = camera()

    ## configurar camara y pines
    picam2 = cam.config()
    seteo_pines()

    ## obtener modelo
    modelo, etiquetas = cam.get_model(model_path, label_path)
    detalles_IN = cam.get_input_details(modelo)
    height_wind, width_wind, indices_IN = cam.get_params(detalles_IN)

    # Ejecutar la aplicación
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

    while True:
        im= picam2.capture_array()
        image = cam.modificar_img(im, width_wind, height_wind)
        fps, last_time = calculo_fps(last_time)
        detecciones = cam.resultados(modelo, image, indices_IN, im, etiquetas)

        # Convertir la imagen a base64
        _, buffer = cv2.imencode('.jpg', im)
        image_data = base64.b64encode(buffer).decode('utf-8')

        # Enviar la imagen a través de Socket.IO
        socketio.emit('video_feed', image_data)

        cv2.putText(im, f'FPS: {fps:.2f} | Vehicles: {len(detecciones)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

        sincronizar_LEDs(len(detecciones))

        socketio.run(app, host='0.0.0.0', port=5000, debug=True)

        key = cv2.waitKey(1)
        if key == 27:
            break

cv2.destroyAllWindows()
GPIO.cleanup() # Limpieza de pines GPIO 
