# video_flawer

This python package is create to add artificial defects to videos: camera shake, auto focus blur, and noise simulation.

## Installation

Via pip:

> pip install video_flawer

## Usage as utility

To flaw a video (with path `./test.mp4') with preset deffects call:

> python -m video_flawer test.mp4

The output (for example `/data/out.avi') file can be setup as:

> python -m video_flawer test.mp4 /data/out.avi

For customization of video defects you should create your custom config file (JSON format). You can provide the file (for example `./my_config.json` as follows:

> python -m video_flawer text.mp4 /data/out.avi my_config.json


## Usage in script

You can use `video_flawer` directly in your script with preset defects as follows


```python
import video_flawer

INPUT_PATH = "test.mp4"
OUTPUT_PATH = "out.avi"

video_flawer.run(INPUT_PATH, OUTPUT_PATH)
```

The defect details can be provided as nested dictionary

```python
import video_flawer

INPUT_PATH = "test.mp4"
OUTPUT_PATH = "out.avi"

CONFIG = {
    "shift_sin_x": {
        "max_shift": 3,
        "frequency": 0.25
    },
}

video_flawer.run(INPUT_PATH, OUTPUT_PATH, config_data=CONFIG)
```

Or the defects can be described in JSON file:

```python
import video_flawer

INPUT_PATH = "test.mp4"
OUTPUT_PATH = "out.avi"

video_flawer.run(INPUT_PATH, OUTPUT_PATH, config_path="config_example.json")
```

## Known issues

* The output files are way too big. This issue should be addressed in future.
* The implemented effects are not well explained.

## Preset defects

The sample JSON file with default settings follows

```json
{
    "crop": {
        "w": 80,
        "h": 20
    },
    "shift_sin_x": {
        "max_shift": 3,
        "frequency": 0.25
    },
    "shift_sin_y": {
        "max_shift": 3,
        "frequency": 0.1
    },
    "shift_random_x": {
        "max_shift": 5,
        "max_duration": 2,
        "min_shift": 1,
        "min_duration": 0.5
    },
    "shift_random_y": {
        "max_shift": 5,
        "max_duration": 2,
        "min_shift": 1,
        "min_duration": 0.5
    },
    "rotation_sin": {
        "max_deg": 1,
        "frequency": 0.1
    },
    "rotation_random": {
        "max_deg": 2,
        "max_duration": 1,
        "min_deg": 1,
        "min_duration": 0.3
    },
    "scale_sin": {
        "max_percentage": 0.5,
        "frequency": 0.1
    },
    "scale_random": {
        "max_percentage": 1,
        "max_duration": 5,
        "min_percentage": 1,
        "min_duration": 3
    },
    "af_blur": {
        "blur_amount": 15,
        "duration": 1,
        "interval": 3
    },
    "white_noise": {
        "noise_min": -50,
        "noise_max": 50,
        "appear_possibility": 0.1
    },
    "line_noise": {
        "appear_possibility": 0.0005,
        "min_line_length": 0.3,
        "max_line_length": 1
    }
}
```







