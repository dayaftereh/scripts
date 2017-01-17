import os
import json
import logging

_DEFAULT_CONFIG_DIR = "config"
_DEFAULT_CONFIG_NAME = "config.json"
_DEFAULT_LOG_CONFIG_NAME = "default_log.json"


######################################################################################################

def load(path):
    json_content = _load_json(path)
    logging.info("loaded configuration from [ %s ]", path)

    config = Configuration(json_content)
    return config


def _load_json(path):
    with file(path) as f:
        content = json.load(f)
        return content


def get_default_config(path):
    conf_dir = get_config_dir(path)
    conf_file = os.path.join(conf_dir, _DEFAULT_CONFIG_NAME)
    return os.path.abspath(conf_file)


def get_config_dir(path):
    dirname = os.path.dirname(path)
    config_dir = os.path.join(dirname, _DEFAULT_CONFIG_DIR)
    return os.path.abspath(config_dir)


def get_default_log_config(path):
    conf_dir = get_config_dir(path)
    conf_file = os.path.join(conf_dir, _DEFAULT_LOG_CONFIG_NAME)
    return os.path.abspath(conf_file)


######################################################################################################

class ConfigurationException(Exception):
    def __init__(self, message, *args):
        self.args = args
        self.message = message

    def _to_string(self):
        if self.args:
            return str(self.message) % self.args
        return str(self.message)

    def __str__(self):
        return self._to_string()


######################################################################################################

class Configuration:
    def __init__(self, content):
        self._content = content

    ######################################################################################################

    def get(self, key):
        value = self.get_default(key, None)
        if value is None:
            raise ConfigurationException("can't find configuration key [ %s ] in configuration file [ %s ]",
                                         key,
                                         self._path)
        return value

    def get_default(self, key, default_value=None):
        self._valid_content()
        path = map(lambda x: x.strip(), key.split('.'))
        value = self._find(self._content, path)
        if value is None:
            return default_value
        return value

    ######################################################################################################

    def as_int(self, key):
        value = self.get(key)
        return int(value)

    def as_int_default(self, key, default_value=None):
        value = self.get_default(key, default_value)
        return int(value)

    def as_float(self, key):
        value = self.get(key)
        return float(value)

    def as_float_default(self, key, default_value=None):
        value = self.get_default(key, default_value)
        return float(value)

    def as_string(self, key):
        value = self.get(key)
        return str(value)

    def as_string_default(self, key, default_value):
        value = self.get_default(key, default_value)
        return str(value)

    ######################################################################################################

    def _valid_content(self):
        if self._content is None:
            raise ConfigurationException("configuration content is empty or not loaded!")

    def _find(self, element, path):
        if not path:
            return element
        next_key = path[0]
        if next_key in element:
            path.remove(next_key)
            next_element = element[next_key]
            return self._find(next_element, path)
        return None
