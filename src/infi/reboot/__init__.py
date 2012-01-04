__import__("pkg_resources").declare_namespace(__name__)

import os
import time
import json
import psutil
import ctypes
import math

from logging import getLogger
log = getLogger()

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
        self.uptime = self._get_current_uptime()
        self._basedir = basedir

    def _get_key_filepath(self):
        return os.path.join(self._basedir, '.'.join(["infi", "reboot", "request", self._name]))

    def has_taken_place(self):
        if not os.path.exists(self._get_key_filepath()):
            # For POSIX operating systems, /tmp is persistent across reboots, so this
            log.debug("key file {!r} does not exist, thus a reboot took place".format(self._get_key_filepath()))
            return True
        previous_timestamp = self._get_timestamp_from_key_file()
        previous_uptime = self._get_uptime_from_key_file()
        log.debug("current timestamp = {}, recorded timestamp = {}".format(self.timestamp, previous_timestamp))
        log.debug("current uptime = {}, recorded uptime = {}".format(self.uptime, previous_uptime))
        if previous_uptime > self.uptime:
            log.debug("uptime is low, thus a reboot took place")
            return True
        elif self.timestamp - self.uptime > previous_timestamp - previous_uptime:
            log.debug("more than just uptime has passed since the reboot, thus a reboot took place")
            return True
        log.debug("a reboot did not take place")
        return False

    def _get_content_from_key_file(self):
        with open(self._get_key_filepath(), 'r') as fd:
            resultdict = json.load(fd)
            return resultdict

    def _get_timestamp_from_key_file(self):
        return self._get_content_from_key_file()['timestamp']

    def _get_uptime_from_key_file(self):
        return self._get_content_from_key_file()['uptime']

    def _get_current_timestamp(self):
        return int(time.time())

    def _get_current_uptime(self):
        if os.name == 'nt':
            dll = ctypes.windll.kernel32
            func = getattr(dll, 'GetTickCount64', getattr(dll, 'GetTickCount'))
            return int(func() / 1000)
        elif os.path.exists('/proc/uptime'):
                with open('/proc/uptime') as fd:
                    return int(fd.read().splitlines()[0].split([0]))
        else:
            return self._get_current_timestamp() - int(psutil.Process(0).create_time)

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
            json.dump(dict(timestamp=self.timestamp, uptime=self.uptime), fd, indent=4)

def ask_for_reboot(key):
    Request(key).make_request()

def has_reboot_took_place(key):
    return Request(key).has_taken_place()

