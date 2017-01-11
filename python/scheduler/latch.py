import time
import threading

class Latch:

    def __init__(self, count):
        self._count = count
        self._condition = threading.Condition()

    def count_down(self):
        with self._condition:
            self._count = self._count - 1
            if self._count <= 0:
                self._condition.notify_all()

    def _wait_with_timeout(self, timeout):
        with self._condition:
            start = time.time()
            while self._count > 0:
                self._condition.wait(timeout)
                if (time.time() - start) > timeout:
                    return False
        return True

    def wait(self, timeout=None):
        if timeout:
            return self._wait_with_timeout(float(timeout))

        with self._condition:
            while self._count > 0:
                self._condition.wait()
        return True
