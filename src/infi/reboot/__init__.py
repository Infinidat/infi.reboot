__import__("pkg_resources").declare_namespace(__name__)

import os
import time
import json

from infi.pyutils.lazy import cached_method

class Request(object):
    def __init__(request_key):
        super(Request, self).__init__()
        self._name = name

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
            return True
        if self._get_current_uptime() < self._get_uptime_from_key_file():
            return True
        if self._get_current_uptime() < self._get_expected_uptime_if_no_reboot_ocurred():
            return True

    def _get_expected_uptime_if_no_reboot_ocurred(self):
        return self._get_uptime_from_key_file() + self._get_current_time() - self._get_time_from_key_file()

    def _get_snapshot_from_key_file(self):
        with open(self._get_key_filepath(), 'r') as fd:
            resultdict = json.load(fd)
            return resultdict

    def _get_time_from_key_file(self):
        return self._get_snapshot_from_key_file['time']

    def _get_uptime_from_key_file(self):
        return self._get_snapshot_from_key_file['uptime']

    def _get_current_time(self):
        return time.time()

    def _get_system_boot_time(self):
        from psutil import BOOT_TIME
        return BOOT_TIME

    def _get_current_uptime(self):
        return self._get_current_time() - self._get_current_time()

    def make_request(self):
        self._remove_key_file()
        self._write_snapshot_to_key_file()

    def _remove_key_file(self):
        path = self._get_key_filepath()
        if not os.path.exists(path):
            os.remove(path)

    def _write_snapshot_to_key_file(self):
        path = self._get_key_filepath()
        with open(path, 'w') as fd:
            json.dump(dict(uptime=self._get_current_uptime(),
                           time=self._get_current_time(), indent=4), fd)

def ask_for_reboot(key):
    Request(key).make_request()

def has_reboot_took_place(key):
    return Request(key).has_taken_place()

