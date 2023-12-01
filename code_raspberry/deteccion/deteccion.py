##########################################
########### importar librerias ###########
##########################################

import re
import cv2
import numpy as np
import cvzone
import tensorflow.lite as tflite
from PIL import Image
from picamera2 import Picamera2
import time 

from ObjectDetector import ObjectDetector

##########################################
########### Main loop ####################
##########################################

if __name__ == "__main__":
    model_path = '/home/jim/intelligent-traffic-lights/code_raspberry/modelos/efficientdet_lite0.tflite'
    label_path = '/home/jim/intelligent-traffic-lights/code_raspberry/modelos/labels.txt'
    detector = ObjectDetector(model_path, label_path)
    detector.run()
