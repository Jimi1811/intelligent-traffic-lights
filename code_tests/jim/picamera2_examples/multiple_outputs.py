from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput

import time

# Create an instance of the Picamera2 class
picam2 = Picamera2()
# Create a video configuration for the camera
video_config = picam2.create_video_configuration()
# Configure the camera with the created video configuration
picam2.configure(video_config)

# Create an H.264 encoder with repeat set to True and I-frame period (iperiod) set to 15
encoder = H264Encoder(repeat=True, iperiod=15)

# Create an FfmpegOutput for streaming to a network address (replace <ip-address> with the actual IP address)
output1 = FfmpegOutput("-f mpegts udp://127.0.0.1:5000")
output1.timestamp = True

# Create a FileOutput for recording to a file
output2 = FileOutput()
output2.timestamp = True  # Set timestamp for file recording

# Set the encoder's output to include both network streaming and file recording
encoder.output = [output1, output2]

# Start encoding and streaming to the network
picam2.start_encoder(encoder)

# Start the camera
picam2.start()

# Wait for 5 seconds
time.sleep(5)

# Start recording to a file (test.h264)
output2.fileoutput = "test.h264"
output2.start()

# Wait for 5 seconds
time.sleep(5)

# Stop recording to the file
output2.stop()

# The file is closed, but continue streaming to the network
# (Note: The following line introduces a sleep duration of a very long time, but it's commented out with a comment indicating its purpose)
# Uncomment and adjust as needed for your specific use case
time.sleep(9999999)
