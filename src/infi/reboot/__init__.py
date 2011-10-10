__import__("pkg_resources").declare_namespace(__name__)

import os
import time
import json
import logging

from infi.pyutils.lazy import cached_method

class Request(object):
    def __init__(self, request_key):
        super(Request, self).__init__()
        self._name = request_key
        self.time = self._get_current_time()
        self.uptime = self._get_current_uptime()

    def _get_tempdir(self):
        if os.name == "nt":
            return os.environ.get("TEMP", os.path.join(os.environ.get("SYSTEMROOT", r"C:\WINDOWS"), "Temp"))
        else:
            return os.path.join(os.path.sep, 'tmp')

    def _get_key_filepath(self):
        return os.path.join(self._get_tempdir(), '.'.join(["reboot", "request", self._name]))

    def has_taken_place(self):
        if not os.path.exists(self._get_key_filepath()):
            # For POSIX operating systems, /tmp is persistent across reboots, so this is enough
            logging.debug("key file {!r} does not exist, thus a reboot took place".format(self._get_key_filepath()))
            return True
        current = self.uptime
        previous = self._get_uptime_from_key_file()
        if current < previous:
            logging.debug("current uptime {} is lower than uptime from key file {}, thus a reboot took place".format(current, previous))
            return True
        expected = self._get_expected_uptime_if_no_reboot_ocurred()
        if current < expected:
            logging.debug("current uptime {} is lower than expected uptime from key file {}, thus a reboot took place".format(current, expected))
            return True
        logging.debug("current uptime {} is higher than expected uptime from key file {}, thus a reboot did not took place".format(current, expected))
        return False

    def _get_expected_uptime_if_no_reboot_ocurred(self):
        return self._get_uptime_from_key_file() + self.time - self._get_time_from_key_file()

    def _get_snapshot_from_key_file(self):
        with open(self._get_key_filepath(), 'r') as fd:
            resultdict = json.load(fd)
            return resultdict

    def _get_time_from_key_file(self):
        return self._get_snapshot_from_key_file()['time']

    def _get_uptime_from_key_file(self):
        return self._get_snapshot_from_key_file()['uptime']

    def _get_current_time(self):
        return time.time()

    def _get_system_boot_time(self):
        from psutil import BOOT_TIME
        return BOOT_TIME

    def _get_current_uptime(self):
        return self.time - self._get_system_boot_time()

    def make_request(self):
        if os.path.exists(self._get_key_filepath()):
            self._remove_key_file()
        self._write_snapshot_to_key_file()

    def _remove_key_file(self):
        path = self._get_key_filepath()
        if os.path.exists(path):
            os.remove(path)

    def _write_snapshot_to_key_file(self):
        path = self._get_key_filepath()
        with open(path, 'w') as fd:
            json.dump(dict(uptime=self.uptime, time=self.time), fd, indent=4)

def ask_for_reboot(key):
    Request(key).make_request()

def has_reboot_took_place(key):
    return Request(key).has_taken_place()

