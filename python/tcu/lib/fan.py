import time
import logging
import threading


######################################################################################################

def create_and_start(config, gpio):
    fan = Fan(config, gpio)
    fan.start()
    return fan


######################################################################################################

class Fan(threading.Thread):
    def __init__(self, conf, gpio):
        threading.Thread.__init__(self)
        self._run_time = 0
        self._config = conf
        self._running = False
        self._lock = threading.RLock()
        self._gpio = FanGPIO(conf, gpio)

        ######################################################################################################

    def _get_cpu_tmu_threshold(self):
        value = self._config.as_float('fan.thresholds.cpu')
        return value

    def on_cpu_tmu(self, value):
        cpu_tmu_threshold = self._get_cpu_tmu_threshold()
        if value > cpu_tmu_threshold:
            logging.debug("cpu tmu threshold reached with [ %s > %s ].", value, cpu_tmu_threshold)
            self._start_fan()

            ######################################################################################################

    def _get_dht_tmu_threshold(self):
        value = self._config.as_float('fan.thresholds.dht')
        return value

    def on_dht_tmu(self, value):
        dht_tmu_threshold = self._get_dht_tmu_threshold()
        if value > dht_tmu_threshold:
            logging.debug("dht tmu threshold reached with [ %s > %s ].", value, dht_tmu_threshold)
            self._start_fan()

            ######################################################################################################

    def _get_fan_run_time(self):
        value = self._config.as_float('fan.run_time')
        return value

    def _start_fan(self):
        with self._lock:
            self._gpio.start()
            self._run_time = self._get_fan_run_time()
            logging.debug("started gpio fan with run time [ %s s ].", self._run_time)

    def _stop_fan(self):
        self._gpio.stop()
        logging.debug("stopped gpio fan.")

    def _update(self, delta):
        with self._lock:
            if self._run_time < 0:
                return

            self._run_time -= delta
            if self._run_time < 0:
                self._stop_fan()

    ######################################################################################################

    def start(self):
        self.name = "Fan Controller Thread"
        logging.debug("starting fan controller...")
        with self._lock:
            self._running = True
        self._start_fan()
        threading.Thread.start(self)

    def is_running(self):
        with self._lock:
            return self._running

    def stop(self):
        logging.debug("stopping fan controller...")
        with self._lock:
            self._running = False

    ######################################################################################################

    def run(self):
        logging.info("fan controller as been started.")
        while self.is_running():
            time0 = time.time()
            time.sleep(1)
            delta = time.time() - time0
            self._update(delta)

        self._gpio.dispose()
        logging.info("fan controller has been stopped.")


######################################################################################################

class FanGPIO:
    def __init__(self, config, gpio):
        self._gpio = gpio
        self._value = None
        self._config = config

    def _get_pin(self):
        pin = self._config.as_int('fan.pin')
        return pin

    def _write(self, value):
        self._value = value
        pin = self._get_pin()
        self._gpio.digitalWrite(pin, value)

        if self.is_started():
            logging.debug('setting pin [ %s ] to [ HIGH ].', pin)
        elif self.is_stopped():
            logging.debug('setting pin [ %s ] to [ LOW ].', pin)
        else:
            logging.debug('unknown value [ %s ] for pin [ %s ].', value, pin)


            ######################################################################################################

    def initialize(self):
        pin = self._get_pin()
        logging.info('initializing pin [ %s ] for gpio fan controlling...', pin)
        self._gpio.pinMode(pin, self._gpio.OUTPUT)
        logging.debug('setting pin [ %s ] to output mode.', pin)
        self._write(self._gpio.LOW)

        ######################################################################################################

    def is_started(self):
        return self._value is self._gpio.HIGH

    def is_stopped(self):
        return self._value is self._gpio.LOW

    def start(self):
        self._write(self._gpio.HIGH)

    def stop(self):
        self._write(self._gpio.LOW)

        ######################################################################################################

    def dispose(self):
        pin = self._get_pin()
        logging.debug('disposing pin [ %s ] for gpio fan controlling...', pin)
        self.stop()
