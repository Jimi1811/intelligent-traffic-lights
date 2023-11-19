############################################################
######################## importar librerias ################
############################################################

import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2

import RPi.GPIO as GPIO
import time

############################################################
######################## configura de los LEDs #############
############################################################

# Definir pines del rasp
red_led_pin = 17
yellow_led_pin = 18
green_led_pin = 27

# Configurar pines
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_led_pin, GPIO.OUT)
GPIO.setup(yellow_led_pin, GPIO.OUT)
GPIO.setup(green_led_pin, GPIO.OUT)

############################################################
######################## configura la camara ###############
############################################################

# Se usa Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

############################################################
######################## definir rutas #####################
############################################################

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

model_path='/home/pi/tensorflow/efficientdet_lite0.tflite'
label_path='/home/pi/tensorflow/labels.txt'

############################################################
######################## definir funciones #################
############################################################

### cargar etiquetas
def load_labels(label_path):
    r"""Returns a list of labels"""
    with open(label_path) as f:
        labels = {}
        for line in f.readlines():
            m = re.match(r"(\d+)\s+(\w+)", line.strip())
            labels[int(m.group(1))] = m.group(2)
        return labels

### cargar modelo
def load_model(model_path):
    r"""Load TFLite model, returns a Interpreter instance."""
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

### detectar objetos
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
        if score > 0.5:
            result.append({'pos': positions[idx], 'id': classes[idx]})
    return result

### dibujar los bounding boxes
def display_result(result, frame, labels):
    
    for obj in result:
        pos = obj['pos']
        id = obj['id']
        x1 = int(pos[1] * CAMERA_WIDTH)
        x2 = int(pos[3] * CAMERA_WIDTH)
        y1 = int(pos[0] * CAMERA_HEIGHT)
        y2 = int(pos[2] * CAMERA_HEIGHT)
        d=labels[id]
        
		# Incrementar el conteo del objeto detectado
        object_count[d] += 1

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0),1)
        cvzone.putTextRect(frame,f'{d}',(x1,y1),1,1)

    cv2.imshow('Object Detection', frame)

### Definir la sincronizacion de los semaforos
def Poco_trafico():
		GPIO.output(green_led_pin, GPIO.HIGH)
	    time.sleep(30)
	    GPIO.output(green_led_pin, GPIO.LOW)
	    GPIO.output(yellow_led_pin, GPIO.HIGH)
	    time.sleep(5)
	    GPIO.output(yellow_led_pin, GPIO.LOW)
	    GPIO.output(red_led_pin, GPIO.HIGH)
	    time.sleep(30)
	    GPIO.output(red_led_pin, GPIO.LOW)
def Mucho_trafico():
		GPIO.output(green_led_pin, GPIO.HIGH)
	    time.sleep(10)
	    GPIO.output(green_led_pin, GPIO.LOW)
	    GPIO.output(yellow_led_pin, GPIO.HIGH)
	    time.sleep(5)
	    GPIO.output(yellow_led_pin, GPIO.LOW)
	    GPIO.output(red_led_pin, GPIO.HIGH)
	    time.sleep(10)
	    GPIO.output(red_led_pin, GPIO.LOW)
def traffic_light_sequence():
	if car_count >= 10:
	    Mucho_trafico()
	else:
		Poco_trafico()


############################################################
######################## Main loop #########################
############################################################

if __name__ == "__main__":

		try:
			### inicializacion
		    model_path = 'efficientdet_lite0.tflite'
		    label_path = 'labels.txt'
		    interpreter = load_model(model_path)
		    labels = load_labels(label_path)
		
		    input_details = interpreter.get_input_details()
		
		    ### Get Width and Height
		    input_shape = input_details[0]['shape']
		    height = input_shape[1]
		    width = input_shape[2]
		
		    ### Get input index
		    input_index = input_details[0]['index']
		
			### Inicializar el diccionario de conteo
		    object_count = {label: 0 for label in labels.values()}
		
		    ### Mantiene la camara encendida
		    while True:
				# captura de frames
		        im= picam2.capture_array()
		        im=cv2.flip(im,-1)
		        image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
		        image = image.resize((width, height))
		
				# objeto detectados
		        top_result = process_image(interpreter, image, input_index)
		
		        # mostrar resultados
				display_result(top_result, im, labels)

				# Mostrar el conteo
				print("Conteo de objetos detectados:")
				for label, count in object_count.items():
				    print(f"{label}: {count}")

				traffic_light_sequence(object_count['car'])

				# condicion de paro
		        key = cv2.waitKey(1)
		        if key == 27:  # esc
		            break
		
		except KeyboardInterrupt:
			# Manejo de la interrupción por teclado (Ctrl+C)
		    print("Programa detenido por el usuario.")
				
		finally:
	    	### Limpieza de recursos
	    	cv2.destroyAllWindows()
			### Limpia los pines GPIO al salir del programa
	    	GPIO.cleanup()
			### detiene la camara
	    	picam2.stop()
