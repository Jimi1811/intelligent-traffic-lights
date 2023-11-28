import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2
import time

class ObjectDetector:
    def __init__(self):
        self.last_count_time = time.time()
        self.fps = 0.0
    
    def process_image(self, image, input_index):
        input_data = np.expand_dims(image, axis=0)
        self.interpreter.set_tensor(input_index, input_data)
        self.interpreter.invoke()

        output_details = self.interpreter.get_output_details()

        positions = np.squeeze(self.interpreter.get_tensor(output_details[0]['index']))
        classes = np.squeeze(self.interpreter.get_tensor(output_details[1]['index']))
        scores = np.squeeze(self.interpreter.get_tensor(output_details[2]['index']))

        result = []

        for idx, score in enumerate(scores):
            if score > 0.5:
                result.append({'pos': positions[idx], 'id': classes[idx]})

        return result
    
    def display_result(self, result, frame, classes_of_interest=["bus", "truck", "car"]):
        for obj in result:
            pos = obj['pos']
            id = obj['id']
            d = self.labels[id]
            if d in classes_of_interest:
                x1 = int(pos[1] * 320)
                x2 = int(pos[3] * 320)
                y1 = int(pos[0] * 480)
                y2 = int(pos[2] * 480)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cvzone.putTextRect(frame, f'{d}', (x1, y1), 1, 1)
        cv2.imshow('Object Detection', frame)

    def calculate_fps(self):
        current_time = time.time()
        loop_time = current_time - self.last_count_time
        self.fps = 0.9 * self.fps + 0.1 * (1 / loop_time)
        self.last_count_time = current_time
        return self.fps