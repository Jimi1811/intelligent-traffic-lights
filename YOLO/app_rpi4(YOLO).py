#################################################################
##################### Importar librerias ########################
#################################################################

from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from picamera import PiCamera
import base64
import io

import cv2
import numpy as np


#################################################################
##################### Cargar el detector ########################
#################################################################

# Configuración de OpenCV con YOLOv3
# descargar yolo3.weights --> https://pjreddie.com/media/files/yolov3.weights
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getUnconnectedOutLayersNames()

#################################################################
##################### Inicializar aplicacion ####################
#################################################################

app = Flask(__name__) # instancia de la app desarrollada en FLASK
socketio = SocketIO(app) # instancia para la comunicacion en tiempo real
camera = PiCamera() # instancia para la interaccion con la camara raspberry pi

#################################################################
##################### Definir funcion para detectar objetos######
#################################################################

def detect_objects(frame):
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 2:  # Class ID 2 corresponds to "car" in COCO dataset
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            frame = cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

#################################################################
##################### Definir rutas #############################
#################################################################

# ruta para la plantilla principal
@app.route('/')
def index():
    return render_template('index.html')

# conectar el cliente
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado.')

# generar el stream (envio de fotogramas)
def generate_stream():
    while True:
        # Capturar un fotograma desde el módulo de cámara
        frame = np.empty((camera.resolution[1] * camera.resolution[0] * 3,), dtype=np.uint8)
        camera.capture(frame, 'bgr')
        frame = frame.reshape((camera.resolution[1], camera.resolution[0], 3))

        # Realizar la detección de vehículos
        frame_with_detection = detect_objects(frame)

        # Convertir el fotograma con detección a base64
        _, buffer = cv2.imencode('.jpg', frame_with_detection)
        frame_data = base64.b64encode(buffer).decode('utf-8')

        # Enviar el fotograma a través de WebSockets
        socketio.emit('livestream', {'frame': frame_data})

# ruta para la recepcion del video
@app.route('/video_feed')
def video_feed():
    return Response(generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

#################################################################
##################### Ejecucion #################################
#################################################################

if __name__ == '__main__':
    camera.start_preview()  # Iniciar vista previa de la cámara
    socketio.start_background_task(target=generate_stream) # generar stream
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) # correr la app
