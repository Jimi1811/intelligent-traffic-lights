import cv2
import numpy as np
import tensorflow.lite as tflite

class ObjectDetection:
    def __init__(self):
        self.detector = detector

    def load_labels(label_path):
        r"""Returns a list of labels"""
        with open(label_path) as f:
            labels = {}
            for line in f.readlines():
                m = re.match(r"(\d+)\s+(\w+)", line.strip())
                labels[int(m.group(1))] = m.group(2)
            return labels   

    def load_model(model_path):
        r"""Load TFLite model, returns a Interpreter instance."""
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter 
    
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
                result.append({'pos': positions[idx], 'id': classes[idx]})
        return result
    
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
