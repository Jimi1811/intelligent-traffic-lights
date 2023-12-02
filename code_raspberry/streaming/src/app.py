from flask import Flask, render_template, Response
import io
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder, H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput
from threading import Condition
import time
from datetime import datetime

class Camera:
    def __init__(self):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_video_configuration(main={"size": (640, 480)}))
        self.encoder = JpegEncoder()
        self.file_out = FfmpegOutput('test2.mp4', audio=False)  # StreamingOutput()
        self.stream_out = StreamingOutput()
        self.stream_out2 = FileOutput(self.stream_out)
        self.encoder.output = [self.file_out, self.stream_out2]

        self.camera.start_encoder(self.encoder)
        self.camera.start()

        self.recording = False  # Agregamos un indicador de grabación

    def start_recording(self):
        if not self.recording:
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            video_filename = f"{current_time}.mp4"
            self.file_out.filename = video_filename
            self.camera.start_recording(self.encoder, self.file_out)
            self.recording = True

    def stop_recording(self):
        if self.recording:
            self.camera.stop_recording()
            self.recording = False

    def get_frame(self):
        self.camera.start()
        with self.stream_out.condition:
            self.stream_out.condition.wait()
            frame = self.stream_out.frame
        return frame


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


# defines the function that generates our frames
camera = Camera()


def gen_frames():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(10)  # Espera 10 segundos entre cada frame

# Inicia la grabación al ejecutar el script
camera.start_recording()

try:
    # Inicia la aplicación Flask
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(debug=False, host='0.0.0.0', port=5000)

finally:
    # Detén la grabación cuando la aplicación Flask se detiene
    camera.stop_recording()
