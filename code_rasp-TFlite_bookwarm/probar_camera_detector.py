######## importar lbrerias ######

import re
import picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FfmpegOutput
import io
from flask import Flask, Response
from flask_restful import Resource, Api
from threading import Condition
import cv2
import numpy as np
import socketio
import cvzone
import time
from PIL import Image
import tensorflow.lite as tflite

#######3 inicializar aplicacion #####

app = Flask(__name__)
api = Api(app)
sio = socketio.Server(cors_allowed_origins='*')
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

##### creacion de la clase camera #####

class Camera:
    def __init__(self):
        self.camera = picamera2.Picamera2()
        self.camera.resolution = (640, 480)
        self.stream = io.BytesIO()
        self.frame = None # variable que almacena la img codificada
        self.condition = Condition()

    def capture_frame(self):
        self.camera.capture(self.stream, format='jpeg', use_video_port=True)
        data = np.frombuffer(self.stream.getvalue(), dtype=np.uint8) # convierte a numpy
        self.frame = cv2.imdecode(data, 1) # decodifica la img
        self.stream.seek(0) 
        self.stream.truncate() 

	# agregar metodo __del__

##### creacion de la clase object detector ####

class ObjectDetector:
    def __init__(self, model_path, label_path, camera_width=480, camera_height=320):
        self.CAMERA_WIDTH = camera_width
        self.CAMERA_HEIGHT = camera_height

        self.model_path = model_path
        self.label_path = label_path

        self.interpreter = self.load_model()
        self.labels = self.load_labels()

        input_details = self.interpreter.get_input_details()
        input_shape = input_details[0]['shape']
        self.height = input_shape[1]
        self.width = input_shape[2]
        self.input_index = input_details[0]['index']

        self.last_time = time.time()
        self.fps = 0
        self.last_count_time = time.time()  # Initialize the last time counted

    def load_labels(self):
        with open(self.label_path) as f:
            labels = {}
            for line in f.readlines():
                m = re.match(r"(\d+)\s+(\w+)", line.strip())
                labels[int(m.group(1))] = m.group(2)
            return labels

    def load_model(self):
        interpreter = tflite.Interpreter(model_path=self.model_path)
        interpreter.allocate_tensors()
        return interpreter

    def process_image(self, image):
        input_data = np.expand_dims(image, axis=0)
        self.interpreter.set_tensor(self.input_index, input_data)
        self.interpreter.invoke()

        output_details = self.interpreter.get_output_details()

        positions = np.squeeze(self.interpreter.get_tensor(output_details[0]['index']))
        classes = np.squeeze(self.interpreter.get_tensor(output_details[1]['index']))
        scores = np.squeeze(self.interpreter.get_tensor(output_details[2]['index']))

        result = []

        for idx, score in enumerate(scores):
            if score > 0.3:
                result.append({'pos': positions[idx], 'id': classes[idx]})
        return result

    def display_result(self, result, frame, classes_of_interest=["bus", "truck", "car"]):
        global last_count_time
        for obj in result:
            pos = obj['pos']
            id = obj['id']
            d = self.labels[id]
            if d in classes_of_interest:
                x1 = int(pos[1] * self.CAMERA_WIDTH)
                x2 = int(pos[3] * self.CAMERA_WIDTH)
                y1 = int(pos[0] * self.CAMERA_HEIGHT)
                y2 = int(pos[2] * self.CAMERA_HEIGHT)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cvzone.putTextRect(frame, f'{d}', (x1, y1), 1, 1)
        cv2.imshow('Object Detection', frame)
    def run(self):
        while True:
            im = self.picam2.capture_array()
            im = cv2.flip(im, -1)
            image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
            image = image.resize((self.width, self.height))

            current_time = time.time()
            loop_time = current_time - self.last_time
            self.fps = 0.9 * self.fps + 0.1 * (1 / loop_time)

            top_result = self.process_image(image)
            cv2.putText(im, f'FPS: {self.fps:.2f} | Vehicles: {len(top_result)}',
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

            self.display_result(top_result, im)

            self.last_time = current_time
            key = cv2.waitKey(1)
            if key == 27:  # esc
                break

        cv2.destroyAllWindows()

# Crear instancias de la cámara y el detector de objetos
camera = Camera()
object_detector = ObjectDetector()

# Modificar la función genFrames para utilizar el detector de objetos
def genFrames():
    while True:
        camera.capture_frame()
        frame = camera.frame

        # Utilizar el detector de objetos para obtener la información de detección
        object_info = object_detector.detect_objects(frame)

        # Transmitir el frame y la información de detección a través de socketIO
        sio.emit('frame', {'image': cv2.imencode('.jpg', frame)[1].tobytes(), 'object_info': object_info})

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n\r\n')

# Manejar eventos de socketIO
@sio.event
def connect(sid, environ):
    print(f"Cliente {sid} conectado")

@sio.event
def disconnect(sid):
    print(f"Cliente {sid} desconectado")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
