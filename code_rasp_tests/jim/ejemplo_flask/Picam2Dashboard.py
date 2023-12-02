from flask import Flask, render_template, jsonify, Response, request
from picamera2 import Picamera2
import time
import io
import numpy as np
import cv2

app = Flask(__name__)

# Initialize the camera with default settings
picam2 = Picamera2()
picam2.options["quality"] = 95
picam2.options["framerate"] = 30
picam2.options["resolution"] = (640, 480)
picam2.start()

def generate_frames():
    """Generate frames for the video feed."""
    while True:
        frame = picam2.capture_array("main")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if frame is not None:
            frame = cv2.resize(frame, (640, 480))
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Provide the video feed."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
