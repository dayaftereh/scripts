from utils import ffmpeg


def from_to(src, start, end):
    ffmpeg.fast_exec(
        src,
        [
            "-ss", str(start),
            "-codec", "copy",
            "-to", str(end)
        ])


def from_duration(src, start, duration):
    ffmpeg.fast_exec(
        src,
        [
            "-ss", str(start),
            "-codec", "copy",
            "-t", str(duration)
        ])
