import subprocess

DEFAULT_BUFFER_SIZE = 2 ** 16


class PProcess:
    def __init__(self, exe, pipe=None):
        self._p = None
        self._pipe = pipe
        self._executable = exe

    def execute(self, args):
        cmd = [self._executable] + args
        print " ".join(cmd)
        self._p = subprocess.Popen(cmd,
                                   stdout=self._pipe,
                                   stderr=self._pipe,
                                   bufsize=DEFAULT_BUFFER_SIZE)
        return self

    def get_std_out(self):
        if self._p:
            return self._p.stdout
        return None

    def get_std_error(self):
        if self._p:
            return self._p.stderr
        return None

    def get_std_in(self):
        if self._p:
            return self._p.stdin
        return None

    def communicate(self):
        if self._p:
            return self._p.communicate()

    def wait_for(self):
        if self._p:
            return self._p.wait()

    def exit_code(self):
        if self._p:
            return self._p.returncode
