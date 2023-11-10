# server_web.py (AWS EC2)
from flask import Flask, render_template
from flask_socketio import SocketIO

app_web = Flask(__name__)
socketio_web = SocketIO(app_web)

@app_web.route('/')
def index():
    return render_template('index.html')

@socketio_web.on('connect')
def handle_connect():
    print('Cliente conectado en el servidor web.')

if __name__ == '__main__':
    socketio_web.run(app_web, host='0.0.0.0', port=5001, debug=True)
