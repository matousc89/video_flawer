import sys

from video_flawer.flawer import run

INPUT_PATH = sys.argv[1]
try:
    OUTPUT_PATH = sys.argv[2]
except:
    OUTPUT_PATH = "out.avi"

try:
    CONFIG_PATH = sys.argv[3]
except:
    CONFIG_PATH = False

run(INPUT_PATH, OUTPUT_PATH, config_path=CONFIG)