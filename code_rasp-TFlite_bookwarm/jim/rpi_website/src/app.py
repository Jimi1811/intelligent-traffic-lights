from flask import Flask, render_template, Response
import io
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Condition

class CameraHandler:
    def __init__(self):
        self.picam2 = None
        self.output = StreamingOutput()

    def configure_camera(self):
        if not self.picam2:
            self.picam2 = Picamera2()
            self.picam2.configure(self.picam2.create_video_configuration(main={"size": (640, 480)}))
            self.picam2.start_recording(JpegEncoder(), FileOutput(self.output))

    def get_frame(self):
        with self.output.condition:
            self.output.condition.wait()
            frame = self.output.frame
        return frame

    def stop_recording(self):
        if self.picam2:
            self.picam2.stop_recording()

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class WebApp:
    def __init__(self, camera_handler):
        self.app = Flask(__name__)
        self.camera_handler = camera_handler
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/video_feed', 'video_feed', self.video_feed)
        self.app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)

    def index(self):
        return render_template('index.html')

    def generate(self):
        try:
            while True:
                self.camera_handler.configure_camera()
                frame = self.camera_handler.get_frame()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        finally:
            self.camera_handler.stop_recording()

    def video_feed(self):
        return Response(self.generate(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    camera_handler = CameraHandler()
    web_app = WebApp(camera_handler)
