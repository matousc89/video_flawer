import random

import numpy as np

def img_add(base, m):
    base = base.astype(np.float64)
    out = base + m
    out[out > 255] = 255
    out[out < 0] = 0
    return out.astype(np.uint8)

def gen_sin_wave(frame_num, max_amp=5, frequency=0.5):
    wave = max_amp * np.sin(np.arange(0, frequency * frame_num, frequency))
    return wave

def gen_random_wave(frame_num, fps, max_amp=5, max_duration=5, min_amp=1, min_duration=0.5):
    wave = np.zeros((frame_num))
    begin = 0
    while begin < frame_num:
        m = random.uniform(min_amp, max_amp)
        f = random.uniform(min_duration * fps, max_duration * fps)
        x = np.linspace(0, np.pi, f)
        w = random.choice([-1, 1]) * m * np.sin(x)

        if begin + w.shape[0] > frame_num:
            write_size = frame_num - begin
        else:
            write_size = w.shape[0]

        wave[begin:begin + write_size] = w[:write_size]
        begin += write_size

    return wave


def gen_blur_wave(frame_num, fps, blur_amount, duration, interval):
    wave = np.zeros((frame_num))

    tmp = -1

    begin = 0
    while begin < frame_num:
        x = np.linspace(0, np.pi, duration * fps)
        w1 = np.sin(x) * blur_amount

        x = np.linspace(0, np.pi, duration * fps * 0.5)
        w2 = np.sin(x) * blur_amount * 0.5

        if tmp == -1:
            tmp = w1.shape[0] + w2.shape[0]

        w = np.concatenate((w1, w2, np.zeros((int(fps * interval)))))

        if begin + w.shape[0] > frame_num:
            write_size = frame_num - begin
        else:
            write_size = w.shape[0]

        wave[begin:begin + write_size] = w[:write_size]
        begin += write_size

    return wave.astype(int)

def add_white_noise(frame, noise_min, noise_max, appear_possibility):
    appear_amount = int(frame.size * appear_possibility)
    o = np.ones(appear_amount)
    z = np.zeros(int(frame.size - appear_amount))
    appear_mask = np.concatenate((o, z))
    np.random.shuffle(appear_mask)
    appear_mask = appear_mask.reshape((frame.shape))

    noise_points = np.random.randint(noise_min, noise_max, frame.shape)
    noise_points = appear_mask * noise_points

    return img_add(frame, noise_points)

def add_line_noise(frame, appear_possibility, min_line_length, max_line_length):
    h, w, _ = frame.shape
    noise_lines = np.random.choice(a=[True, False], size=frame.shape[1], p=[appear_possibility, 1 - appear_possibility])
    for i in range(w):
        if not noise_lines[i]:
            continue

        line_length = int(random.uniform(min_line_length * h, max_line_length * h))
        up_point = int(random.uniform(0, h - line_length))
        frame = frame.astype(np.int)
        frame[up_point:up_point + line_length, i] += int(random.choice([-1, 1]) * random.uniform(10, 30))

    frame[frame > 255] = 255
    frame[frame < 0] = 0

    return frame.astype(np.uint8)


def add_pattern_noise(frame, pattern, appear_posibility, min_amount, max_amount, min_size, max_size, alpha):
    if random.random() > appear_posibility:
        return frame

    pattern = pattern.astype(np.float64)

    amount = int(random.uniform(min_amount, max_amount))

    for i in range(amount):
        size = int(random.uniform(min_size, max_size))
        pattern = cv2.resize(pattern, (size, size))

        ph, pw, _ = pattern.shape
        fh, fw, _ = frame.shape

        rot_mat = cv2.getRotationMatrix2D(((pw - 1) / 2.0, (ph - 1) / 2.0), random.random() * 360, 1)
        pattern = cv2.warpAffine(pattern, rot_mat, (pw, ph))

        h = int(random.uniform(0, fh))
        w = int(random.uniform(0, fw))

        ph, pw, _ = frame[h:h + ph, w:w + pw].shape

        frame[h:h + ph, w:w + pw] = img_add(frame[h:h + ph, w:w + pw],
                                            random.choice([-1, 1]) * pattern[:ph, :pw] * alpha)

    return frame


def crop(frame, crop_w, crop_h):
    height, weight, c = frame.shape
    out = np.zeros((height - crop_h * 2, weight - crop_w * 2, c), dtype=np.uint8)

    out = frame[crop_h:-crop_h, crop_w:-crop_w]

    return out