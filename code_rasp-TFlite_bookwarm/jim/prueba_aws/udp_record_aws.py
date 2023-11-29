from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

import socket
import time

# Create an instance of the Picamera2 class
picam2 = Picamera2()

# Create a video configuration for the camera
video_config = picam2.create_video_configuration()
# Configure the camera with the created video configuration
picam2.configure(video_config)

# Create an H.264 encoder with repeat set to True and I-frame period (iperiod) set to 15
encoder = H264Encoder(repeat=True, iperiod=15)

# Create an FfmpegOutput for streaming to a network address
ec2_ip = "3.16.218.231"
ec2_port = 5000  # Change to the port your Flask app is running on
output = FfmpegOutput(f"-f mpegts udp://{ec2_ip}:{ec2_port}")
output.timestamp = True

# Set the encoder's output to network streaming
encoder.output = output

# Start encoding and streaming to the network
picam2.start_encoder(encoder)

# Start the camera
picam2.start()

try:
    while True:
        # Continue streaming indefinitely
        time.sleep(1)

except KeyboardInterrupt:
    # Stop the camera and encoder if the script is interrupted
    picam2.stop()
    picam2.stop_encoder()
