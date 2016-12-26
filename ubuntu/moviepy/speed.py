from utils import ffmpeg


def change(src, speed):
    speed = 1.0 / speed
    ffmpeg.fast_exec(
        src,
        [
            "-an",
            "-filter:v",
            "setpts=%s*PTS" % speed
        ])


def change_fps(src, speed, fps):
    speed = 1.0 / speed
    ffmpeg.fast_exec(
        src,
        [
            "-r", str(fps),
            "-an",
            "-filter:v",
            "setpts=%s*PTS" % speed
        ])
