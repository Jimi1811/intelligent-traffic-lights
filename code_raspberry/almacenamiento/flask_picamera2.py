import picamera2 #camera module for RPi camera
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder, H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput
import io

import subprocess
from flask import Flask, Response
from flask_restful import Resource, Api, reqparse, abort
import atexit
from datetime import datetime
from threading import Condition
import time 

app = Flask(__name__)
api = Api(app)

class Camera:
	def __init__(self):
		self.camera = picamera2.Picamera2()
		self.camera.configure(self.camera.create_video_configuration(main={"size": (640, 480)}))
		self.encoder = JpegEncoder()
		self.fileOut = FfmpegOutput('test2.mp4', audio=False) #StreamingOutput()
		self.streamOut = StreamingOutput()
		self.streamOut2 = FileOutput(self.streamOut)
		self.encoder.output = [self.fileOut, self.streamOut2]
		
		self.camera.start_encoder(self.encoder) 
		self.camera.start() 
		
	def get_frame(self):	
		self.camera.start()
		with self.streamOut.condition:
			self.streamOut.condition.wait()
			self.frame = self.streamOut.frame
		return self.frame

class StreamingOutput(io.BufferedIOBase):
	def __init__(self):
		self.frame = None
		self.condition = Condition()

	def write(self, buf):
		with self.condition:
			self.frame = buf
			self.condition.notify_all()
		
#defines the function that generates our frames
camera = Camera()

def genFrames():
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            
#defines the route that will access the video feed and call the feed function
class VideoFeed(Resource):
	def get(self):
		return Response(genFrames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

class StartRec(Resource):
	def get(self):
		camera.start_recording()
		return {'Status': 'True'}
		
class StopRec(Resource):
	def get(self):
		camera.stop_recording()
		return {'Status': 'True'}
		
api.add_resource(VideoFeed, '/cam')
api.add_resource(StartRec, '/start_rec')
api.add_resource(StopRec, '/stop_rec')
# api.add_resource(convVid, '/picam/convert_vid/<ID>')


if __name__ == '__main__':
	app.run(debug = False, host = '0.0.0.0', port=5000)
