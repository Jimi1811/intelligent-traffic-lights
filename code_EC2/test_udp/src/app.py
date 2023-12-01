from flask import Flask, render_template, Response
import imageio
import requests
import cv2

app = Flask(__name__)

video_stream_url = "http://proxy21.rt3.io:38479"

def generate_frames():
    while True:
        try:
            response = requests.get(video_stream_url, stream=True)
            reader = imageio.get_reader(response.content, 'ffmpeg', mode='I', input_params=["-f", "mpegts", "-"])
            
            for frame in reader:
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    break

                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        except Exception as e:
            print(f"Error: {e}")
            continue

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
