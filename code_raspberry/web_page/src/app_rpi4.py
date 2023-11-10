from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from picamera import PiCamera
import base64
import io

app = Flask(__name__)
socketio = SocketIO(app)
camera = PiCamera()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado.')

def generate_stream():
    while True:
        # Capturar un fotograma desde el módulo de cámara
        frame = io.BytesIO()
        camera.capture(frame, format='jpeg')
        frame.seek(0)

        # Convertir el fotograma a base64
        frame_data = base64.b64encode(frame.read()).decode('utf-8')
        frame.seek(0)

        # Enviar el fotograma a través de WebSockets
        socketio.emit('livestream', {'frame': frame_data})

@app.route('/video_feed')
def video_feed():
    return Response(generate_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    camera.start_preview()  # Iniciar vista previa de la cámara
    socketio.start_background_task(target=generate_stream)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
