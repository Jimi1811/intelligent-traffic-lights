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
red_led_pin = 17 # semaforo rojo
yellow_led_pin = 18 # semaforo ambar
green_led_pin = 27 # semaforo verde

# Configurar pines
GPIO.setmode(GPIO.BCM) 
GPIO.setup(red_led_pin, GPIO.OUT) # seteo rojo
GPIO.setup(yellow_led_pin, GPIO.OUT) # seteo ambar
GPIO.setup(green_led_pin, GPIO.OUT) # seteo verde

############################################################
######################## configura la camara ###############
############################################################

# Se usa Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640,480) # dimensionar la vista
picam2.preview_configuration.main.format = "RGB888" # formato de la vista 8 bits/canal
picam2.preview_configuration.align() 
picam2.configure("preview")
picam2.start() # inicializar camara

############################################################
######################## definir rutas #####################
############################################################

width = 640
height = 480

model_path='/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm/efficientdet_lite0.tflite' # colocar ruta modelo
label_path='/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm/labels.txt'# colocar ruta etiquetas

############################################################
######################## definir funciones #################
############################################################

### cargar etiquetas
def load_labels(label_path):
    r"""Returns a list of labels"""
    with open(label_path) as f:
        labels = {} # diccioonario de etiquetas {id:__, class:__}
        for line in f.readlines():
            m = re.match(r"(\d+)\s+(\w+)", line.strip())
            labels[int(m.group(1))] = m.group(2)
        return labels # returna el diccionario de etiquetas

### cargar modelo
def load_model(model_path):
    r"""Load TFLite model, returns a Interpreter instance."""
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors() # transformarlo a tensor
    return interpreter

### detectar objetos
def process_image(interpreter, image, input_index):
    r"""Process an image, Return a list of detected class ids and positions"""
    input_data = np.expand_dims(image, axis=0)  # expandir el frame a 4 dimensiones (tensor)

    # Process
    interpreter.set_tensor(input_index, input_data) 
    interpreter.invoke() # se realiza la deteccion como tal

    # Get outputs
    output_details = interpreter.get_output_details() # obtener info de las detecciones
	    # output_details[0]['name']: El nombre del tensor.
	    # output_details[0]['shape']: La forma del tensor (nÃºmero de dimensiones y tamaÃ±o en cada dimensiÃ³n).
	    # output_details[0]['dtype']: El tipo de datos del tensor (por ejemplo, np.float32).
	    # output_details[0]['index']: El Ã­ndice del tensor que se utilizarÃ¡ con mÃ©todos como interpreter.get_tensor().

    positions = np.squeeze(interpreter.get_tensor(output_details[0]['index'])) # vectores de posicion
    classes = np.squeeze(interpreter.get_tensor(output_details[1]['index'])) # clases detectadas
    scores = np.squeeze(interpreter.get_tensor(output_details[2]['index'])) # puntuaciones detectadas

    result = [] 

    for idx, score in enumerate(scores):
        if score > 0.5:
            result.append({'pos': positions[idx], 'id': classes[idx]})
				    #    result = [
					#	    {'pos': [0.1, 0.2, 0.5, 0.8], 'id': 3},
					#	    {'pos': [0.4, 0.6, 0.7, 0.9], 'id': 2}
					#	]
    return result # retorna solo las detecciones confiables {posicion, clase}

### dibujar los bounding boxes
def display_result(result, frame, labels, fps):
    
    for obj in result:
        pos = obj['pos']
        id = obj['id']
        x1 = int(pos[1] * CAMERA_WIDTH)
        x2 = int(pos[3] * CAMERA_WIDTH)
        y1 = int(pos[0] * CAMERA_HEIGHT)
        y2 = int(pos[2] * CAMERA_HEIGHT)
        d=labels[id] # Utiliza la identificaciÃ³n de la clase (id) para obtener 
        			 # la etiqueta de la clase (d) desde el diccionario de etiquetas (labels).
        
		# Incrementar el conteo de vehiculos detectados
        if d == 2 or d == 5 or d == 7: # si detecta carros, buses o camiones
            object_count[d] += 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0),1)
            
            text_1 = f'vehicle -- {confidence:.2%}'  # Agrega la etiqueta de la clase y 
                                                                     # el porcentaje de confiabilidad al texto
                                                                     # considerando 2 decimales
            text_2 = f'FPS: {fps:.2f}'  # Agrega el FPS								   					 
            cvzone.putTextRect(frame, text_1, (x1, y1), 1, 1)
            cvzone.putTextRect(frame, text_2, (0, 0), 1, 1)
            
    cv2.imshow('Object Detection', frame)
    N_carros = object_count[d]
    return N_carros

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
	if car_count >= 5:
	    Mucho_trafico()
	else:
		Poco_trafico()


############################################################
######################## Main loop #########################
############################################################


if __name__ == "__main__":
	
	try:
		interpreter = load_model(model_path)
		labels = load_labels(label_path)

		input_details = interpreter.get_input_details()

		input_shape = input_details[0]['shape']
		height = input_shape[1]
		width = input_shape[2]

		input_index = input_details[0]['index']
		start_time = 0 # inicializa el tiempo
		
		### Mantiene la camara encendida
		while True:
			# captura de frames
			im= picam2.capture_array()
			im=cv2.flip(im,-1)
			image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
			image = image.resize((width, height))

	
			# objeto detectados
			top_result = process_image(interpreter, image, input_index)
					# top_result = [
					# {'pos': [y1, x1, y2, x2], 'id': clase1, 'confidence': confianza1},
					# {'pos': [y1, x1, y2, x2], 'id': clase2, 'confidence': confianza2},
					# # ... otros objetos detectados ...
					# ]
	
			# Calcular el tiempo transcurrido
			elapsed_time = time.time() - start_time

			# Calcular los FPS
			fps = frame_count / elapsed_time
	
			# mostrar resultados
			display_result(top_result, im, labels, fps)

			# Incrementar el contador de cuadros
			frame_count += 1

			# Mostrar los FPS en la consola
			print(f"FPS: {fps:.2f}")

			# Mostrar el conteo y accionar LEDs
			print("Conteo de objetos detectados:")
			for label, count in object_count.items(): # dict_items([('Persona', 3), ('AutomÃ³vil', 5), ('CamiÃ³n', 2)])
				if label == 'car' or label == 'truck':
					print(f"{label}: {count}")
					traffic_light_sequence(object_count[label])

			# condicion de paro
			key = cv2.waitKey(1)
			if key == 27:  # esc
				break
	
	except KeyboardInterrupt:
		# Manejo de la interrupciÃ³n por teclado (Ctrl+C)
		print("Programa detenido por el usuario.")
			
	finally:
		### Limpieza de recursos
		cv2.destroyAllWindows()
		### Limpia los pines GPIO al salir del programa
		GPIO.cleanup()
		### detiene la camara
		picam2.stop()