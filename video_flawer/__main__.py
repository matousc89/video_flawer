import sys

from video_flawer.flawer import run

INPUT_PATH = sys.argv[1]
try:
    OUTPUT_PATH = sys.argv[2]
except:
    OUTPUT_PATH = "out.avi"

try:
    CONFIG = sys.argv[3]
except:
    CONFIG = False

run(INPUT_PATH, OUTPUT_PATH, CONFIG)