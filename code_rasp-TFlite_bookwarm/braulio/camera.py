import cv2
import socketio
import base64
import threading

sio = socketio.Client()

class Camera:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)  # Puedes cambiar el índice si la cámara no es la predeterminada
        self.sio = sio

    def start_streaming(self):
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            _, img_encoded = cv2.imencode('.jpg', frame)
            image_str = base64.b64encode(img_encoded).decode('utf-8')

            self.sio.emit('stream', {'image': image_str})

    def stop_streaming(self):
        self.video_capture.release()

# Conectar a la instancia de SocketIO
@sio.event
def connect():
    print('Conectado al servidor')

@sio.event
def disconnect():
    print('Desconectado del servidor')

if __name__ == "__main__":
    camera = Camera()

    # Iniciar hilo de streaming
    streaming_thread = threading.Thread(target=camera.start_streaming)
    streaming_thread.start()

    # Conectar al servidor SocketIO
    sio.connect('http://tu_servidor_socketio:puerto')
