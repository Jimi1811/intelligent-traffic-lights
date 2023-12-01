import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.preview_configuration.main.size = (480,320)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate=30
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

CAMERA_WIDTH = 480
CAMERA_HEIGHT = 320

model_path='/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm/braulio/modelos/efficientdet_lite0.tflite'
label_path='/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm/braulio/modelos/labels.txt'

## retorna etiquetas
def load_labels(label_path):
    r"""Returns a list of labels"""
    with open(label_path) as f:
        labels = {}
        for line in f.readlines():
            m = re.match(r"(\d+)\s+(\w+)", line.strip())
            labels[int(m.group(1))] = m.group(2)
        return labels

## retorna modelo
def load_model(model_path):
    r"""Load TFLite model, returns a Interpreter instance."""
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

## detecta y devuelva una lista de detecciones
def process_image(interpreter, image, input_index):
    r"""Process an image, Return a list of detected class ids and positions"""
    input_data = np.expand_dims(image, axis=0)  # expand to 4-dim

    # Process
    interpreter.set_tensor(input_index, input_data)
    interpreter.invoke()

    # Get outputs
    output_details = interpreter.get_output_details()

    positions = np.squeeze(interpreter.get_tensor(output_details[0]['index']))
    classes = np.squeeze(interpreter.get_tensor(output_details[1]['index']))
    scores = np.squeeze(interpreter.get_tensor(output_details[2]['index']))

    result = []

    for idx, score in enumerate(scores):
        if score > 0.3:
            result.append({'pos': positions[idx], 'id': classes[idx], 'confidence': scores[idx]})
    return result

## muestra en pantalla los carros detectados
def display_result(result, frame, labels, classes_of_interest=["bus", "truck", "car"]):
    global last_count_time
    for obj in result:
          pos = obj['pos']
          id = obj['id']
          score = obj['confidence']
          d = labels[id]
          if d in classes_of_interest:
               x1 = int(pos[1] * CAMERA_WIDTH)
               x2 = int(pos[3] * CAMERA_WIDTH)
               y1 = int(pos[0] * CAMERA_HEIGHT)
               y2 = int(pos[2] * CAMERA_HEIGHT)
               cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0),1)
               cvzone.putTextRect(frame,f'carro | {int(score*100)}%',(x1,y1),1,1)
    cv2.imshow('Object Detection', frame)

if __name__ == "__main__":
     #model_path = 'efficientdet_lite0.tflite'
     #label_path = 'labels.txt'
     interpreter = load_model(model_path)
     labels = load_labels(label_path)
     
     input_details = interpreter.get_input_details()
     input_shape = input_details[0]['shape']
     height = input_shape[1]
     width = input_shape[2]
     input_index = input_details[0]['index']
     
     last_time = time.time() # inicializar el tiempo actual
     fps = 0 # inicializar la tasa de fps
     Num_vehiculos = 0 # inicializar la cantidad de vehiculos
     nivel = "bajo" # inicializar el nivel de trafico
     
     while True:
          # vehicle_count = 0
          im= picam2.capture_array()
          #im=cv2.flip(im,-1)
          image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
          image = image.resize((width, height))
          
          current_time = time.time()
          hora_actual = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # hora actual
          loop_time = current_time - last_time
          fps = 0.9*fps + 0.1*(1/(loop_time))
          
          ## realizar detecciones
          top_result = process_image(interpreter, image, input_index)
          Num_vehiculos = len(top_result)
          
          if int(loop_time) % 10 == 0 and int(loop_time) != 0: # cada 10 segundos
                ## estimar el nivel de trafico
                if Num_vehiculos < 3:
                    nivel = "bajo"
                elif Num_vehiculos < 7 and Num_vehiculos >= 3:
                    nivel = "medio"
                elif Num_vehiculos >= 7:
                    nivel = "alto"


          #cv2.putText(im, f'FPS: {fps:.2f} | Carros: {len(top_result)}',
          #             (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
          cv2.putText(im, f'cantidad Carros: {len(top_result)}',
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
          cv2.putText(im, f'nivel: {nivel}',
                    (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
          cv2.putText(im, f'Tiempo transcurrido: {int(loop_time)} segundos',
                        (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
          cv2.putText(im, f'{hora_actual}',
                        (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
          
          ## mostrar resultados
          display_result(top_result, im, labels)
          
          #last_time = current_time # al descomentarlo te cuenta los fps como debe ser

          ## condicion de paro
          key = cv2.waitKey(1)
          if key == 27:  # esc
               break

cv2.destroyAllWindows()
