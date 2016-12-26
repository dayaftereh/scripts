import process, subprocess, fs
from ffmpeg_exception import FFmpegException

FF_PROBE_EXE = 'ffmpeg'

STDOUT_CONSOLE = None
STDOUT_PIPE = subprocess.PIPE


def execute(args, pipe=STDOUT_PIPE):
    check_ffmpeg()
    p = process.PProcess(FF_PROBE_EXE, pipe)
    return p.execute(args)


def fast_exec(path, args):
    path = fs.file_exists(path)
    output = fs.catch_output(path)

    p = execute([
                    '-i', path,
                    '-y'
                ]
                + args
                + [output],
                STDOUT_CONSOLE)

    exit_code = p.wait_for()
    if exit_code != 0:
        ex_string = "ffmpeg exists with code [ %s ] while processing file [ %s ], please check the standard error output" % (
            exit_code, path
        )
        raise FFmpegException(ex_string)

    return output


def check_ffmpeg():
    path = fs.which(FF_PROBE_EXE)
    if not path:
        ex_string = "no %s has been found on the system, please install %s" % (FF_PROBE_EXE, FF_PROBE_EXE)
        raise FFmpegException(ex_string)
