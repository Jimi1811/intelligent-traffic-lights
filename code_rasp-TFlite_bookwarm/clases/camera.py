import cv2
from object_detector import ObjectDetector
from picamera2 import PiCamera2
import tensorflow.lite as tflite
from PIL import Image
import time

global Num_vehiculos

model_path = '/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm/clases/efficientdet_lite0.tflite'
label_path = '/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm//clases/labels.txt'

class Camera:
    def __init__(self, label_path, model_path):
        ## inicializar variables
        self.frame_count = 0
        self.start_time = time.time()
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

    ## inicializamos detector de objetos
    object_detector = ObjectDetector()

    ## inicializamos camara
    camera = Camera(label_path, model_path)
    start_time = camera.start_time

    ## obtenemos parametros
    labels = camera.load_labels(label_path)
    model = camera.load_model(model_path)
    height, width, input_shape, input_index = camera.params(model)

    while True:
        try:
            # modificar camara
            im = camera.capture_array()
            im = cv2.flip(im,-1)
            image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
            image = image.resize((width, height))

            # mostrar tiempo
            elapsed_time = time.time() - start_time ## tiempo transcurrido
            # mins, secs = divmod(elapsed_time, 60) ## obtener minutos y segundos
            # hours, mins = divmod(mins, 60) ## obtener horas y minutos
            # timer_str = "{:02}:{:02}:{:02}".format(int(hours), int(mins), int(secs)) ## tiempo en formato string
            # print("\rTiempo transcurrido: {}".format(timer_str), end="") 
            # time.sleep(1) 

            # deteccion de objetos cada 75 segundos
            if elapsed_time >= 75: 
                start_time = 0
                objects = object_detector.process_image(image, input_index) # Ejecuta la lógica de detección de objetos
                object_detector.display_result(objects, image) # muestra los resultados
                cv2.putText(im, f'FPS: {fps:.2f} | Vehicles: {len(objects)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                Num_vehículos = len(objects)

            # calculo de fps
            fps = object_detector.calculate_fps() # calcula los fps
            cv2.putText(im, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
            
            # Limpia el búfer de captura para la siguiente imagen
            camera.truncate(0) 


        except:
            break

        finally:
            camera.close()
