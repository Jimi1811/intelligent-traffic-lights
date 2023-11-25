from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_frame')
def handle_video_frame(frame):
    # Procesa el frame como desees
    print(f"Received video frame: {len(frame)} bytes")
    # Envía el frame a todos los clientes conectados
    socketio.emit('video_frame', frame)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
