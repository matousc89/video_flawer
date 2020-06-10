import os
import json

import numpy as np
import cv2

from video_flawer.effects import crop
from video_flawer.effects import add_pattern_noise
from video_flawer.effects import add_line_noise
from video_flawer.effects import add_white_noise
from video_flawer.effects import gen_blur_wave
from video_flawer.effects import gen_random_wave
from video_flawer.effects import gen_sin_wave


def run(INPUT_PATH, OUTPUT_PATH="out.avi", config_data=None, config_path=None):

    # get default config if the config is not provided

    if config_data is None and config_path is None:
        config_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = "{}/config.json".format(config_dir)
        with open(config_path) as json_file:
            config = json.load(json_file)

    elif not config_path is None:
        with open(config_path) as json_file:
            config = json.load(json_file)

    else:
        config = config_data



    # Create a VideoCapture object
    cap = cv2.VideoCapture(INPUT_PATH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    if "pattern_noise" in config:
        pattern_img = []
        c_patterns = config["pattern_noise"]["pattern"]
        for i, c in enumerate(c_patterns):
            pattern_img.append(cv2.imread(c["filename"]))

    # Tremor
    shift_x = np.zeros((frame_num))
    shift_y = np.zeros((frame_num))

    if "shift_sin_x" in config:
        c = config["shift_sin_x"]
        shift_x += gen_sin_wave(frame_num, c["max_shift"], c["frequency"])

    if "shift_sin_y" in config:
        c = config["shift_sin_y"]
        shift_y += gen_sin_wave(frame_num, c["max_shift"], c["frequency"])

    if "shift_random_x" in config:
        c = config["shift_random_x"]
        shift_x += gen_random_wave(frame_num, fps, c["max_shift"], c["max_duration"], c["min_shift"], c["min_duration"])

    if "shift_random_y" in config:
        c = config["shift_random_y"]
        shift_x += gen_random_wave(frame_num, fps, c["max_shift"], c["max_duration"], c["min_shift"], c["min_duration"])


    # Rotation
    rotation_deg = np.zeros((frame_num))

    if "rotation_sin" in config:
        c = config["rotation_sin"]
        rotation_deg += gen_sin_wave(frame_num, c["max_deg"], c["frequency"])

    if "rotation_random" in config:
        c = config["rotation_random"]
        rotation_deg += gen_random_wave(frame_num, fps, c["max_deg"], c["max_duration"], c["min_deg"],
                                        c["min_duration"])

    # Scale
    scale_percentage = np.zeros((frame_num))

    if "scale_sin" in config:
        c = config["scale_sin"]
        scale_percentage += gen_sin_wave(frame_num, c["max_percentage"], c["frequency"])

    if "scale_random" in config:
        c = config["scale_random"]
        scale_percentage += gen_random_wave(frame_num, fps, c["max_percentage"], c["max_duration"], c["min_percentage"],
                                            c["min_duration"])

    # af blur
    if "af_blur" in config:
        c = config["af_blur"]
        blur_deg = gen_blur_wave(frame_num, fps, c["blur_amount"], c["duration"], c["interval"])


    # Crop
    if "crop" in config:
        crop_w = config["crop"]["w"]
        crop_h = config["crop"]["h"]
    else:
        crop_w, crop_h = 0, 0


    # filesize problem: https://stackoverflow.com/questions/38686359/opencv-videowriter-control-bitrate
    codec = "DIVX"
    out = cv2.VideoWriter(OUTPUT_PATH, cv2.VideoWriter_fourcc(*codec), fps, (width - crop_w * 2, height - crop_h * 2))

    # TODO: allow to use FFMPEG
    # from video_writter import VideoWritter
    # out = VideoWritter(OUTPUT_PATH)

    # processing
    frame_counter = 0
    while True:
        ret, frame = cap.read()

        if ret == True:

            # Tremor
            M_rotate = cv2.getRotationMatrix2D(((width - 1) / 2.0, (height - 1) / 2.0), rotation_deg[frame_counter], 1)
            M_shift = np.float32([[0, 0, shift_x[frame_counter]],
                                  [0, 0, shift_y[frame_counter]]])
            M_scale = np.float32([[(100 + scale_percentage[frame_counter]) / 100, 1, 1],
                                  [1, (100 + scale_percentage[frame_counter]) / 100, 1]])
            M = (M_shift + M_rotate) * M_scale
            frame_processed = cv2.warpAffine(frame, M, (width, height))

            # crop
            if "crop" in config:
                frame_processed = crop(frame_processed, crop_w, crop_h)

            # blur
            if "af_blur" in config:
                if blur_deg[frame_counter] != 0:
                    frame_processed = cv2.blur(frame_processed,
                                               (blur_deg[frame_counter], blur_deg[frame_counter]))

            # noise
            if "white_noise" in config:
                c = config["white_noise"]
                frame_processed = add_white_noise(frame_processed, c["noise_min"],
                                                  c["noise_max"], c["appear_possibility"])

            if "line_noise" in config:
                c = config["line_noise"]
                frame_processed = add_line_noise(frame_processed, c["appear_possibility"],
                                                 c["min_line_length"], c["max_line_length"])

            # noise_pattern
            if "pattern_noise" in config:
                c_patterns = config["pattern_noise"]["pattern"]
                for i, c in enumerate(c_patterns):
                    frame_processed = add_pattern_noise(frame_processed, pattern_img[i], c["appear_possibility"],
                                                        c["min_amount"], c["max_amount"], c["min_size"], c["max_size"],
                                                        c["alpha"])

            out.write(frame_processed)

        # Break the loop
        else:
            break

        frame_counter += 1

    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()

