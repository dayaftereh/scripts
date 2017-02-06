#!/usr/bin/python

import logging
import os
import random
import threading

import config
import wpi2_gpio


#########################################################################################

def binary_2_decimal(bit_string):
    return int(bit_string, 2)


def binary_add(*args):
    p = bin(sum(int(str(x), 2) for x in args))[2:]
    while len(p) < 8:
        p = "0" + p
    return p


#########################################################################################

class DHT22Exception(Exception):
    def __init__(self, message, *args):
        self.args = args
        self.message = message

    def _to_string(self):
        if self.args:
            return str(self.message) % self.args
        return str(self.message)

    def __str__(self):
        return self._to_string()


#########################################################################################

class DHT22(threading.Thread):
    def __init__(self, conf, gpio):
        super(DHT22, self).__init__()
        self._hooks = []
        self._gpio = gpio
        self._reader = None
        self._config = conf
        self._running = False
        self._last_read = None
        self._lock = threading.RLock()

    def _get_pin(self):
        value = self._config.as_int('dht22.pin')
        return value

    def _get_read_timeout(self):
        value = self._config.as_float("dht22.read_timeout")
        return value

    #########################################################################################

    def _time(self):
        return self._gpio.millis() / 1000.0

    def _notify_all(self, value):
        with self._lock:
            hook_copy = list(self._hooks)

        for hook in hook_copy:
            hook(value)

    #########################################################################################

    def _initialize(self):
        with self._lock:
            pin = self._get_pin()
            self._last_read = self._time()
            self._reader = DHT22Reader(pin, self._gpio)
            self._reader.initialize()
            logging.info("DHT22 has been started")

    def _read_tmu(self):
        try:
            values = self._reader.read()
            logging.debug("DHT22 received data with [ humidity: %s, tmu: %s ]", *values)
            return values[1]
        except DHT22Exception:
            logging.exception('DHT22 failed while reading:')
        return None

    def _update(self):
        with self._lock:
            read_timeout = self._get_read_timeout()
            if (self._last_read + read_timeout) > self._time():
                return
            self._last_read = self._time()
            value = self._read_tmu()
        if value is not None:
            self._notify_all(value)

    def _dispose(self):
        with self._lock:
            self._reader.dispose()
        logging.info("DHT22 has been stopped")

    #########################################################################################

    def add_hook(self, hook):
        with self._lock:
            self._hooks.append(hook)

    def start(self):
        with self._lock:
            self._running = True
            # super(DHT22, self).start()

    def is_running(self):
        with self._lock:
            return self._running

    def run(self):
        self._initialize()
        # while self._running:
        self._read_tmu()
        self._gpio.delay(500)
        self._dispose()

    def stop(self):
        with self._lock:
            self._running = False


#########################################################################################

class DHT22Timer:
    def __init__(self, gpio):
        self._gpio = gpio
        self._delay_offset = 0

    #########################################################################################

    def time(self):
        return self._gpio.micros()

    def delay_microseconds(self, us):
        time = self.time() + (us - self._delay_offset)
        while self.time() < time:
            pass

    def _clamp(self, vmin, val, vmax):
        return max(vmin, min(vmax, val))

    def calibrate_time(self, loops=10000):
        logging.info("calibrating DHT22 timer for this system...")
        delays = []
        for i in range(loops):
            timeout = random.randrange(1, 100)
            time = self.time()
            self.delay_microseconds(timeout)
            delays.append((self.time() - time) - timeout)
        value = sum(delays) / loops
        self._delay_offset = self._clamp(0, value, 20)
        logging.info("DHT22 timer delay offset is [ %s ]", self._delay_offset)

    #########################################################################################

    def _wait_for_true(self, time_min, time_max, fn):
        if not fn():
            raise DHT22Exception('DHT22 timer failed, because [ %s ] already true', fn)

        time = self.time()
        # self.delay_microseconds(time_min)
        while fn():
            if self.time() > (time + time_max):
                return False

        delta = self.time() - time
        return delta < time_max

    def low_to_high(self, time_min, time_max):
        return self._wait_for_true(time_min, time_max, self._gpio.is_low)

    def high_to_low(self, time_min, time_max):
        return self._wait_for_true(time_min, time_max, self._gpio.is_high)


#########################################################################################


class DHT22GPIO:
    def __init__(self, pin, gpio):
        self._pin = pin
        self._gpio = gpio

    def micros(self):
        return self._gpio.micros()

    #########################################################################################

    def write_low(self):
        self._gpio.digitalWrite(self._pin, self._gpio.LOW)

    def write_high(self):
        self._gpio.digitalWrite(self._pin, self._gpio.HIGH)

    #########################################################################################

    def output_mode(self):
        self._gpio.pinMode(self._pin, self._gpio.OUTPUT)

    def input_mode(self):
        self._gpio.pinMode(self._pin, self._gpio.INPUT)

    #########################################################################################

    def read(self):
        return self._gpio.digitalRead(self._pin)

    def is_low(self):
        value = self._gpio.digitalRead(self._pin)
        return value is self._gpio.LOW

    def is_high(self):
        value = self._gpio.digitalRead(self._pin)
        return value is self._gpio.HIGH


#########################################################################################

class DHT22Reader:
    def __init__(self, pin, gpio):
        self._gpio = DHT22GPIO(pin, gpio)
        self._timer = DHT22Timer(self._gpio)

    #########################################################################################

    def initialize(self):
        logging.debug("initializing DHT22 reader...")
        self._timer.calibrate_time()

    #########################################################################################

    def _send_start(self):
        # send:
        # 1                --- 20 us ---
        # 0 --- 1000 us ---
        self._gpio.output_mode()
        self._gpio.write_low()
        self._timer.delay_microseconds(1000)
        self._gpio.input_mode()
        self._timer.delay_microseconds(30)

    def _wait_for_response(self):

        # receive: response
        # 1              --- 80 us ---
        # 0 --- 80 us ---
        if not self._timer.low_to_high(75, 85):
            raise DHT22Exception("DHT22 reader failed while waiting of start response")

        if not self._timer.high_to_low(75, 85):
            raise DHT22Exception("DHT22 reader failed while waiting of start response")

    def _read_bits(self):
        bit_string = ''
        for i in range(40):
            bit_string += self._read_bit(i + 1)
        return bit_string

    def _read_bit(self, i):
        # receive: bit 0
        # 1              --- 26 us ---
        # 0 --- 50 us ---

        if not self._timer.low_to_high(48, 55):
            raise DHT22Exception("DHT22 reader failed while reading bit [ %s ] from low to high", i)

        if not self._timer.high_to_low(22, 75):
            raise DHT22Exception("DHT22 reader failed while reading bit [ %s ] from high to low", i)

        return '1'

    #########################################################################################

    def _validated_bit_string(self, pairs):
        if not len(pairs) is 5:
            raise DHT22Exception("DHT22 reader failed, because bit string [ %s ] is incorrect", ' '.join(pairs))

        parity_bits0 = pairs[4]
        parity_bits1 = binary_add(pairs[:-1])
        if not parity_bits0 is parity_bits1:
            raise DHT22Exception(
                "DHT22 reader failed, because parity_bits [ %s != %s ] not equals in bit string [ %s ]",
                parity_bits0,
                parity_bits1,
                ' '.join(pairs))

    def _convert_tmu(self, bit_string):
        tmu_raw = int(bit_string, 2)
        tmu_bit_num = len(bit_string)
        tmu_mask = 2 ** (tmu_bit_num - 1)
        tmu = -(tmu_raw & tmu_mask) + (tmu_raw & ~tmu_mask)
        return tmu / 10.0

    def _convert_humidity(self, bit_string):
        humidity = int(bit_string, 2)
        return humidity / 10.0

    def _read_values(self, pairs):
        tmu_bit_str = pairs[2] + pairs[3]
        humidity_bit_str = pairs[0] + pairs[1]
        tmu = self._convert_tmu(tmu_bit_str)
        humidity = self._convert_humidity(humidity_bit_str)
        return humidity, tmu

    #########################################################################################

    def read(self):
        self._send_start()
        self._wait_for_response()
        bit_string = self._read_bits()
        pairs = map(''.join, zip(*[iter(bit_string)] * 2))

        self._validated_bit_string(pairs)
        values = self._read_values(pairs)
        return values

    def dispose(self):
        logging.debug("disposing DHT22 reader...")
        self._gpio.output_mode()
        self._gpio.write_low()


#########################################################################################


def main():
    logging.root.setLevel("DEBUG")
    path = os.path.dirname(os.path.abspath(__file__))
    conf_path = config.get_default_config(path)
    conf = config.load(conf_path)
    gpio = wpi2_gpio.create_and_configure(conf)

    pin = 15

    gpio.pinMode(pin, gpio.OUTPUT)
    gpio.digitalWrite(pin, gpio.LOW)
    gpio.delay(18)

    gpio.pinMode(pin, gpio.INPUT)


    print "piHiPri", gpio.piHiPri(10)
    counter = 0
    bit_str = ''
    loopMax = 10000
    laststate = gpio.LOW
    l = []
    for i in range(84):
        counter = 0
        while gpio.digitalRead(pin) == laststate:
            counter += 1
            if counter == loopMax:
                break
        laststate = gpio.digitalRead(pin)


        if counter >= loopMax:
            break
        # /* ignore first 3 transitions */

        if (i >= 4) and (i % 2 == 0):
            l.append(counter)

            # /* shove each bit into the storage bytes */
            if counter > 13:
                bit_str += '1'
            else:
                bit_str += '0'

    print gpio.piHiPri(0);

    pairs = map(''.join, zip(*[iter(bit_str)] * 8))
    print l
    print pairs
    print counter
    print bit_str
    print len(bit_str)

    if not len(pairs) is 5:
        print ("DHT22 reader failed, because bit string [ %s ] is incorrect" % ' '.join(pairs))
        return

    parity_bits0 = int(pairs[4], 2)
    parity_bits1 = sum(int(str(x), 2) for x in pairs[:-1]) & 0xFF

    if not parity_bits0 == parity_bits1:
        print (
            "DHT22 reader failed, because parity_bits [ %s != %s ] not equals in bit string [ %s ]"%
            (parity_bits0,
            parity_bits1,
            ' '.join(pairs)))

    print int(pairs[0] + pairs[1], 2)
    print int(pairs[2] + pairs[3], 2)



import time

if __name__ == "__main__":
    while True:
        main()
        time.sleep(2.5)
