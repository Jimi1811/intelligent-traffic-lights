#!/usr/bin/python3

# Record
import time
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, JpegEncoder
from picamera2.outputs import FfmpegOutput, FileOutput

#Flask
from flask import Flask, render_template, Response
import io
from threading import Condition

app = Flask(__name__)

def record_video():
    video_filename = current_time.strftime("%Y-%m-%d_%H-%M.mp4")

    encoder = H264Encoder(10000000)
    output = FfmpegOutput(video_filename, audio=False)

    picam2.start_recording(encoder, output)
    time.sleep(10)
    picam2.stop_recording()


if __name__ == "__main__":
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)

    current_time = datetime.now()
    while True:
        record_video()
        time.sleep(1)  # Wait for 1 second before starting the next recording
