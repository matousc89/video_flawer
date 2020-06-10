from video_flawer import flawer

INPUT_PATH = "test.mp4"
OUTPUT_PATH = "out.avi"

CONFIG = {
    "shift_sin_x": {
        "max_shift": 3,
        "frequency": 0.25
    },
}

flawer.run(INPUT_PATH, OUTPUT_PATH, config_data=CONFIG)