import time
import string
import logging
import threading


######################################################################################################

def create_and_start(config):
    cpu_tmu = CPUTemperature(config)
    cpu_tmu.start()
    return cpu_tmu


######################################################################################################

class CPUTemperature(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self._hooks = []
        self._running = False
        self._lock = threading.RLock()
        self._reader = CPUTemperatureReader(config)

    ######################################################################################################

    def _update(self):
        with self._lock:
            tmu = self._reader.read()
            value = tmu / 1000.0
            hook_copy = list(self._hooks)

        for hook in hook_copy:
            hook(value)

    ######################################################################################################

    def is_running(self):
        with self._lock:
            return self._running

    def start(self):
        logging.debug("starting cpu-tmu-reader...")
        self.name = "Cpu-Temperature-Reader"
        with self._lock:
            self._running = True
        threading.Thread.start(self)

    def add_hook(self, hook):
        with self._lock:
            self._hooks.append(hook)

    def stop(self):
        logging.debug("stopping cpu-tmu-reader...")
        with self._lock:
            self._running = False

    def run(self):
        logging.info("cpu-tmu-reader has been started.")
        while self.is_running():
            time.sleep(10.0)
            self._update()
        logging.info("cpu-tmu-reader has been stopped.")


######################################################################################################

class CPUTemperatureReader:
    def __init__(self, config):
        self._config = config

    def _get_path(self):
        path = self._config.as_string('tmu_file')
        return path

    def read(self):
        temps = []
        path = self._get_path()
        with file(path) as f:
            lines = map(string.strip, f.readlines())
            for line in lines:
                values = line.split(':')
                if len(values) > 1:
                    temp = int(values[1])
                    temps.append(temp)

        if not temps:
            return None

        max_temp = max(temps)
        return max_temp
