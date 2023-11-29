import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2
import time 

global nivel

class ObjectDetector:
    ## inicializacion
    def __init__(self, model_path, label_path, camera_width=480, camera_height=320):
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = (camera_width, camera_height)
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.preview_configuration.controls.FrameRate = 30
        self.picam2.preview_configuration.align()
        self.picam2.configure("preview")
        self.picam2.start()

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

        #self.last_time = time.time() # inicializa el tiempo
        self.fps = 0 # incializa fps
        # self.last_count_time = time.time() # Initialize the last time counted

    ## caargar etiquetas
    def load_labels(self):
        with open(self.label_path) as f:
            labels = {}
            for line in f.readlines():
                m = re.match(r"(\d+)\s+(\w+)", line.strip())
                labels[int(m.group(1))] = m.group(2)
            return labels

    ## cargar modelo
    def load_model(self):
        interpreter = tflite.Interpreter(model_path=self.model_path)
        interpreter.allocate_tensors()
        return interpreter

    ## procesar imagen
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
                result.append({'pos': positions[idx], 'id': classes[idx], 'confidence': scores[idx]})
        return result
    
        ### los resultados de deteccion dan un porcentaje de 
        ### confiabilidad entre el 30 y 50%

    ## mostrar resultados
    def display_result(self, result, frame, classes_of_interest=["bus", "truck", "car"]):
        global last_count_time
        for obj in result:
            pos = obj['pos']
            id = obj['id']
            score = obj['confidence']
            d = self.labels[id]
            if d in classes_of_interest:
                x1 = int(pos[1] * self.CAMERA_WIDTH)
                x2 = int(pos[3] * self.CAMERA_WIDTH)
                y1 = int(pos[0] * self.CAMERA_HEIGHT)
                y2 = int(pos[2] * self.CAMERA_HEIGHT)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cvzone.putTextRect(frame, f'carro | {int(score*100)}%', (x1, y1), 1, 1)
        cv2.imshow('Object Detection', frame)

    ## ejecucion
    def run(self):
        last_time = time.time() # inicializa el tiempo
        Num_vehiculos = 0 # inicializar la cantidad de vehiculos
        nivel = "bajo"
        while True:
            ## Leer imagen y preprocesarla
            im = self.picam2.capture_array()
            #im = cv2.flip(im, -1)
            image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
            image = image.resize((self.width, self.height))

            ## obtener temporizador
            current_time = time.time() # tiempo reciente
            hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # hora actual
            loop_time = current_time - last_time # tiempo de bucle

            ## calcular fps
            self.fps = 0.9 * self.fps + 0.1 * (1 / loop_time)
            #self.last_time = current_time
            #current_time = last_time 

            ## realizar detecciones
            top_result = self.process_image(image)
            Num_vehiculos = len(top_result)

            """
            if int(loop_time) % 20 == 0: # cada 20 segundos
                ## estimar el nivel de trafico
                if Num_vehiculos < 5:
                    nivel = "bajo"
                elif Num_vehiculos < 8 and Num_vehiculos >= 5:
                    nivel = "medio"
                elif Num_vehiculos >= 8:
                    nivel = "alto"
            
                ## hacer visualizar la cantidad de FPS y la cantidad de vehiculos
                cv2.putText(im, f'FPS: {self.fps:.2f} | Vehicles: {len(top_result)}',
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)    
                ## hacer visualizar el nivel de trafico
                cv2.putText(im, f'{nivel}',
                        (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)    
                ## dejar pasar 3 segundos
                time.sleep(3000)
            """

            cv2.putText(im, f'Tiempo transcurrido: {int(loop_time)} segundos',
                        (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(im, f'{hora_actual}',
                        (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            ## mostrar resultados
            self.display_result(top_result, im)

            ## condicion de paro
            key = cv2.waitKey(1)
            if key == 27:  # esc
                break

        cv2.destroyAllWindows()
