from exceptions import Exception


class FFmpegException(Exception):
    def __init__(self, message):
        super(FFmpegException, self).__init__(message)
