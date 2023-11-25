import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2
import time

class ObjectDetector:
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

if __name__ == "__main__":
    model_path = '/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm/efficientdet_lite0.tflite'
    label_path = '/home/jim/intelligent-traffic-lights/code_rasp-TFlite_bookwarm//labels.txt'
    detector = ObjectDetector(model_path, label_path)
    detector.run()
