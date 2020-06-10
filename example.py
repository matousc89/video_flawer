# import video_flawer
#
# INPUT_PATH = "test.mp4"
# OUTPUT_PATH = "out.avi"
#
# CONFIG = {
#     "shift_sin_x": {
#         "max_shift": 3,
#         "frequency": 0.25
#     },
# }
#
# video_flawer.run(INPUT_PATH, OUTPUT_PATH, config_data=CONFIG)


# import video_flawer
#
# INPUT_PATH = "test.mp4"
# OUTPUT_PATH = "out.avi"
#
# video_flawer.run(INPUT_PATH, OUTPUT_PATH)

import video_flawer

INPUT_PATH = "test.mp4"
OUTPUT_PATH = "out.avi"

video_flawer.run(INPUT_PATH, OUTPUT_PATH, config_path="config_example.json")