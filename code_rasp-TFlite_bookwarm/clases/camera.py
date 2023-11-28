import cv2
from traffic_light import TrafficLights
from object_detector import ObjectDetector
from picamera2 import PiCamera2
import tensorflow.lite as tflite
from PIL import Image
import time

model_path = '/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm/efficientdet_lite0.tflite'
label_path = '/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm//labels.txt'

class Camera:
    def __init__(self, traffic_lights, object_detector,label_path, model_path):
        ## inicializar otras instancias
        self.traffic_lights = traffic_lights
        self.object_detector = object_detector
        ## inicializar variables
        self.frame_count = 0
        self.start_time = time.time()
        ## obtener configuraciones del modelo
        self.labels = self.load_labels(label_path)
        self.interpreter = self.load_model(model_path)
        ## inicializar camara
        self.camera = PiCamera2()
        self.camera.preview_configuration.main.size = (480,320)
        self.camera.preview_configuration.main.format = "RGB888"
        self.camera.preview_configuration.controls.FrameRate=30
        self.camera.preview_configuration.align()
        self.camera.configure("preview")
        self.camera.start()

    def load_labels(self, label_path):
        with open(label_path) as f:
            labels = {}
            for line in f.readlines():
                m = re.match(r"(\d+)\s+(\w+)", line.strip())
                labels[int(m.group(1))] = m.group(2)
            return labels
        
    def load_model(self, model_path):
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter
    
    def params(self, interpreter):
        input_details = interpreter.get_input_details()
        input_shape = input_details[0]['shape']
        height = input_shape[1]
        width = input_shape[2]
        input_index = input_details[0]['index']
        return height, width, input_shape, input_index

if __name__ == "__main__":
    Num_vehículos = 0 # inicializar la cantidad de vehiculos

    ## inicializamos componentes fisicos y virtuales
    traffic_lights_1 = TrafficLights(red_pin=17, amber_pin=27, green_pin=22)  # Definir los pines para el primer semáforo
    traffic_lights_2 = TrafficLights(red_pin=23, amber_pin=24, green_pin=25)  # Definir los pines para el segundo semáforo
    object_detector = ObjectDetector(label_path, model_path)

    ## inicializamos camara
    camera = Camera(traffic_lights_1, traffic_lights_2, object_detector)
    
    ## obtenemos parametros
    model = camera.load_model(model_path)
    height, width, input_shape, input_index = camera.params(model)

    while True:
        im = camera.capture_array()
        im = cv2.flip(im,-1)
        image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        image = image.resize((width, height))

        objects = object_detector.process_image(image, input_index) # Ejecuta la lógica de detección de objetos
        object_detector.display_result(objects, image) # muestra los resultados
        fps = object_detector.calculate_fps() # calcula los fps
        cv2.putText(im, f'FPS: {fps:.2f} | Vehicles: {len(objects)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        camera.truncate(0) # Limpia el búfer de captura para la siguiente imagen

        # actualizar patron de semaforos
        traffic_lights_1.traffic_light_pattern(len(objects), senal_inicio="verde")
        traffic_lights_2.traffic_light_pattern(len(objects), senal_inicio="rojo")

        key = cv2.waitKey(1)
        if key == 27:  # esc
            break

traffic_lights_1.cleanup()
traffic_lights_2.cleanup()
camera.close()