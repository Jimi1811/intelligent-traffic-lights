from flask import Flask, render_template, Response
import cv2
import socket
import numpy as np
from threading import Thread, Lock

app = Flask(__name__)

# Variables globales para almacenar el último frame recibido
frame = None
frame_lock = Lock()

def receive_frames():
    global frame
    global frame_lock

    # Configura el socket UDP para recibir frames
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 8000))

    while True:
        data, _ = udp_socket.recvfrom(65507)  # Ajusta según el tamaño máximo de tus frames
        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        frame_lock.acquire()
        frame_lock.release()

# Inicia el hilo para recibir frames
receive_thread = Thread(target=receive_frames)
receive_thread.start()

def generate():
    global frame
    global frame_lock

    while True:
        frame_lock.acquire()
        if frame is not None:
            # Convierte el frame a formato JPEG para mostrar en la web
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        frame_lock.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
