import os

from ffmpeg_exception import FFmpegException


def abs_path(path):
    absPath = os.path.abspath(path)
    return absPath


def file_exists(path):
    if not os.path.exists(path):
        ex_string = "file [ %s ] don't exists on file system" % path
        raise FFmpegException(ex_string)

    if not os.path.isfile(path):
        ex_string = "path [ %s ] is not a file" % path
        raise FFmpegException(ex_string)

    return abs_path(path)


def catch_output(src, postfix=''):
    parent = os.path.dirname(src)

    filename = os.path.basename(src)
    name, ext = os.path.splitext(filename)

    counter = 0
    output = os.path.join(parent, "%s_output%s%s" % (name, postfix, ext))
    while (True):
        if not os.path.exists(output):
            return output
        counter += 1
        output = os.path.join(parent, "%s_output_%s%s%s" % (name, counter, postfix, ext))


def is_exec(fpath):
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)


def which(program):
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exec(program):
            return program

    path = os.environ["PATH"]
    paths = map(lambda x: x.strip(), path.split(os.pathsep))

    for path in paths:
        exe_file = os.path.join(path, fname)
        if is_exec(exe_file):
            return exe_file

    return None
