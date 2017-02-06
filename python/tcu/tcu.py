#!/usr/bin/python

import argparse
import logging
import logging.config
import os
import signal
import time
import json

from lib import fan, wpi2_gpio, config, cpu_tmu


##############################################################################################

def arg_parse():
    parser = argparse.ArgumentParser(prog='tcu')
    parser.add_argument('--log', help='set the log level of tcu', default='info')

    default_log_config = config.get_default_log_config(__file__)
    parser.add_argument('--logconfig', help='the path to the logging configuration', default=default_log_config)

    default_config = config.get_default_config(__file__)
    parser.add_argument('--config', help='the path to configuration file', default=default_config)

    parser.add_argument('--pidfile', help='the path to the pidfile', default='/var/run/tcu.pid')

    args = parser.parse_args()
    return parser, args


def load_logging_config(log_level, path):
    level = str(log_level).upper()

    with file(path) as f:
        json_dict = json.load(f)

    logging.config.dictConfig(json_dict)
    logging.root.setLevel(level)
    logging.info("using log level [ %s ]", level)


def write_pidfile(pidfile):
    if os.path.exists(pidfile) and not os.access(pidfile, os.W_OK):
        logging.warning("can't write pidfile [ %s ], because no write permission")
        return

    pid = os.getpid()
    with open(pidfile, 'w') as f:
        f.write(str(pid))

    logging.info("pid file written to [ %s ] with pid [ %s ].", pidfile, pid)


##############################################################################################

def main():
    time0 = time.time()
    parser, args = arg_parse()

    load_logging_config(args.log, args.logconfig)

    write_pidfile(args.pidfile)
    conf = config.load(args.config)

    app = TCUApplication(conf)
    app.start()
    app.register_signals()

    time1 = time.time() - time0
    logging.info('tcu has been started in [ %0.4f s ].', time1)

    app.wait_for_signals()

    app.stop()
    app.wait_for_workers()
    logging.info('good bye.')


##############################################################################################

class TCUApplication:
    def __init__(self, conf):
        self._fan = None
        self._gpio = None
        self._config = conf
        self._cpu_tmu = None
        self._running = False

    def start(self):
        logging.info("starting tcu application...")
        self._running = True
        self._gpio = wpi2_gpio.create_and_configure(self._config)

        # --------------------------
        #self._gpio.pinMode(15, self._gpio.OUTPUT)
        #self._gpio.digitalWrite(15, self._gpio.LOW)
        # --------------------------

        self._fan = fan.create_and_start(self._config, self._gpio)

        self._cpu_tmu = cpu_tmu.create_and_start(self._config)
        self._cpu_tmu.add_hook(self._fan.on_cpu_tmu)

    ##############################################################################################

    def wait_for_signals(self):
        logging.debug('waiting for signals with main-loop...')
        while self._running:
            signal.pause()

    def _on_signal_user_1(self, *args):
        logging.info("received signal user1")
        self._fan.on_cpu_tmu(1000.0)

    def _on_signal_interrupt(self, *args):
        logging.info("received signal interrupt")
        self._running = False

    def _on_signal_termination(self, *args):
        logging.info("received signal termination")
        self._running = False

    def register_signals(self):
        logging.debug("register signals [ SIGUSR1, SIGINT, SIGTERM ]...")
        signal.signal(signal.SIGUSR1, self._on_signal_user_1)
        signal.signal(signal.SIGINT, self._on_signal_interrupt)
        signal.signal(signal.SIGTERM, self._on_signal_termination)

    ##############################################################################################

    def stop(self):
        logging.info('stopping tcu...')
        self._fan.stop()
        self._cpu_tmu.stop()

    def wait_for_workers(self):
        logging.debug('waiting for workers...')
        self._fan.join()
        self._cpu_tmu.join()


##############################################################################################

if __name__ == "__main__":
    main()
