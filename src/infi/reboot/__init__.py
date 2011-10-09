__import__("pkg_resources").declare_namespace(__name__)

import os
import time

from infi.pyutils.lazy import cached_method

class Reqeust(object):
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
        if self.get_current_update < self._get_expected_uptime_if_no_reboot_ocurred():
            return True

    def _get_expected_uptime_if_no_reboot_ocurred(self):
        return self._get_uptime_from_key_file() + self._get_current_time() - self._get_time_from_key_file() 

    def get_snapshot_from_key_file(self):
        raise NotImplementedError()

    def _get_time_from_key_file(self):
        raise NotImplementedError()

    def _get_uptime_from_key_file(self):
        raise NotImplementedError()

    def _get_current_time(self):
        return time.time()

    def _get_current_uptime(self):
        raise NotImplementedError()

    def make_request(self):
        self._remove_key_file()
        self._create_key_file()
        self._write_snapshot_to_key_file()

    def _remove_key_file(self):
        raise NotImplementedError()

    def _create_key_file(self):
        raise NotImplementedError()

    def _write_snapshot_to_key_file(self):
        raise NotImplementedError()

def ask_for_reboot(key):
    raise NotImplementedError()

def has_reboot_took_place(key):
    raise NotImplementedError()

