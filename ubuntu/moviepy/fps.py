from utils import ffmpeg


def transcode(src, fps):
    ffmpeg.fastExec(
        src,
        [
            "-strict",
            "-2",
            "-r", str(fps)
        ])
