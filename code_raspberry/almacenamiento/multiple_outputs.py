from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput
import time
from datetime import datetime


current_time = datetime.now()

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = H264Encoder(repeat=True, iperiod=15)

output1 = FfmpegOutput("-f mpegts udp://127.0.0.1:12345")
output2 = FileOutput()

encoder.output = [output1, output2]
# Start streaming to the network.
picam2.start_encoder(encoder)

picam2.start()
time.sleep(5)
# Start recording to a file.
output2.fileoutput = "test.h264"
output2.start()
time.sleep(5)
output2.stop()
# The file is closed, but carry on streaming to the network.
# time.sleep(9999999)


while True:
    video_filename = current_time.strftime("%Y-%m-%d_%H-%M-%S.mp4")

    encoder = H264Encoder(10000000)
    output = FfmpegOutput(video_filename, audio=False)

    picam2.start_recording(encoder, output)
    time.sleep(10)
    picam2.stop_recording()

    time.sleep(1)  # Wait for 1 second before starting the next recording
