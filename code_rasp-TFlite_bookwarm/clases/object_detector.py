import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2
import time

global CAMERA_WIDTH, CAMERA_HEIGHT
CAMERA_WIDTH = 480
CAMERA_HEIGHT = 320
FRAME_RATE = 30

## Configurar camara
def config_cam():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (CAMERA_WIDTH, CAMERA_HEIGHT)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.controls.FrameRate = FRAME_RATE
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start() 

    return picam2

## cargar etiquetas
def load_labels(label_path):
    with open(label_path) as f:
        labels = {}
        for line in f.readlines():
            m = re.match(r"(\d+)\s+(\w+)", line.strip())
            labels[int(m.group(1))] = m.group(2)
        return labels

## cargar modelo
def load_model(model_path):
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

## realizar deteccion
def process_image(interpreter, image, input_index):
    input_data = np.expand_dims(image, axis=0)
    interpreter.set_tensor(input_index, input_data)
    interpreter.invoke()
    
    output_details = interpreter.get_output_details()
    
    positions = np.squeeze(interpreter.get_tensor(output_details[0]['index']))
    classes = np.squeeze(interpreter.get_tensor(output_details[1]['index']))
    scores = np.squeeze(interpreter.get_tensor(output_details[2]['index']))
    
    result = []
    
    for idx, score in enumerate(scores):
        if score > 0.5:
            result.append({'pos': positions[idx], 'id': classes[idx]})
            
    return result

## imprime resultados en el video
def display_result(result, frame, labels, classes_of_interest=["bus", "truck", "car"]):
    global last_count_time
    for obj in result:
          pos = obj['pos']
          id = obj['id']
          d = labels[id]
          if d in classes_of_interest:
               x1 = int(pos[1] * CAMERA_WIDTH)
               x2 = int(pos[3] * CAMERA_WIDTH)
               y1 = int(pos[0] * CAMERA_HEIGHT)
               y2 = int(pos[2] * CAMERA_HEIGHT)
               cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0),1)
               cvzone.putTextRect(frame,f'{d}',(x1,y1),1,1)
    cv2.imshow('Object Detection', frame)

## calcular FPS
def calculo_fps(last_time):
    current_time = time.time()
    loop_time = current_time - last_time
    fps = 0.9*fps + 0.1*(1/(loop_time))
    last_time = current_time
    return fps, last_time
