# import packages
from PIL import Image
from subprocess import Popen, PIPE
from imutils.video import VideoStream
from imutils.object_detection import non_max_suppression
from imutils import paths
import cv2
import numpy as np
import imutils


class VideoWritter():

    def __init__(self, OUTPUT_PATH):
        self.p = Popen(['ffmpeg', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-r', '24', '-i', '-', '-vcodec', 'h264', '-q:v', '5', '-r', '24', OUTPUT_PATH], stdin=PIPE)

    def write(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        im.save(self.p.stdin, 'JPEG')

    def release(self):
        pass
