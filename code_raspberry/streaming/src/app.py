from flask import Flask, render_template, Response
import io
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Condition

app = Flask(__name__)

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

@app.route('/')
def index():
    return render_template('index.html')

def generate():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (480, 320)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.controls.FrameRate = 30
    picam2.preview_configuration.align()
    picam2.configure("preview")    
    output = StreamingOutput()  
    picam2.start_recording(JpegEncoder(), FileOutput(output))

    try:
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        picam2.stop_recording()

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
