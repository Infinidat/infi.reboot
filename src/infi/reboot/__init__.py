__import__("pkg_resources").declare_namespace(__name__)

import os
import time
import json
import logging
import psutil

PID = 0 if os.name == "nt" else 1

def _get_default_tempdir():
    if os.name == "nt":
        return os.environ.get("TEMP", os.path.join(os.environ.get("SYSTEMROOT", r"C:\WINDOWS"), "Temp"))
    else:
        return os.path.join(os.path.sep, 'var', 'run')

TEMPDIR = _get_default_tempdir()

class Request(object):
    def __init__(self, request_key, basedir=TEMPDIR):
        super(Request, self).__init__()
        self._name = request_key
        self.timestamp = self._get_current_timestamp()
        self._basedir = basedir

    def _get_key_filepath(self):
        return os.path.join(self._basedir, '.'.join(["infi", "reboot", "request", self._name]))

    def has_taken_place(self):
        if not os.path.exists(self._get_key_filepath()):
            # For POSIX operating systems, /tmp is persistent across reboots, so this
            logging.debug("key file {!r} does not exist, thus a reboot took place".format(self._get_key_filepath()))
            return True
        previous = self._get_timestamp_from_key_file()
        logging.debug("current timestamp = {}, recorded timestamp = {}".format(self.timestamp, previous))
        return self.timestamp != previous

    def _get_content_from_key_file(self):
        with open(self._get_key_filepath(), 'r') as fd:
            resultdict = json.load(fd)
            return resultdict

    def _get_timestamp_from_key_file(self):
        return self._get_content_from_key_file()['timestamp']

    def _get_current_timestamp(self):
        return psutil.Process(PID).create_time

    def make_request(self):
        if os.path.exists(self._get_key_filepath()):
            self._remove_key_file()
        self._write_timestamp_to_key_file()

    def _remove_key_file(self):
        path = self._get_key_filepath()
        if os.path.exists(path):
            os.remove(path)

    def _write_timestamp_to_key_file(self):
        path = self._get_key_filepath()
        with open(path, 'w') as fd:
            json.dump(dict(timestamp=self.timestamp), fd, indent=4)

def ask_for_reboot(key):
    Request(key).make_request()

def has_reboot_took_place(key):
    return Request(key).has_taken_place()

