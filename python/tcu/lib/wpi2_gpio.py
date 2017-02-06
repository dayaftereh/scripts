import logging
from wiringpi2 import *

######################################################################################################

def create_and_configure(config):
    wpi_mode = _get_wpi_mode(config)
    gpio = GPIO(wpi_mode)
    return gpio

######################################################################################################

def _get_wpi_mode(config):
    wpi_mode = config.as_int('wpi2_mode')
    logging.debug('using gpio mode [ %s ] for wiring pi setup', wpi_mode)
    return wpi_mode
