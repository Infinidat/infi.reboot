__import__("pkg_resources").declare_namespace(__name__)

import os
import unittest
import logging
import time
from .. import ask_for_reboot, has_reboot_took_place, Request

def random_string(length):
    import random
    import string #pylint: disable-msg=W0402

    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set, length))


def debug_request(request):
    logging.debug("current_time = {}".format(request._get_current_time()))
    logging.debug("current_uptime = {}".format(request._get_current_uptime()))
    logging.debug("key_file = {}".format(request._get_snapshot_from_key_file()))

class RequestTest(unittest.TestCase):
    def test_get_time(self):
        request = Request(None)
        self.assertIsInstance(request._get_current_time(), float)

    def test_get_uptime(self):
        request = Request(None)
        self.assertLess(request._get_current_uptime(), request._get_current_time())

    def test_get_uptime(self):
        request = Request(None)
        now = request._get_current_uptime()
        later = request._get_current_uptime()
        self.assertLess(abs(later - now), 2.01)

    def test_request_works(self):
        random_key = random_string(6)
        request = Request(random_key)
        self.assertTrue(request.has_taken_place())
        request.make_request()
        self.assertFalse(request.has_taken_place())
        request._remove_key_file()
        self.assertFalse(os.path.exists(request._get_key_filepath()))
        self.assertTrue(request.has_taken_place())

class RequestMockTest(unittest.TestCase):
    def test_reboot_always_took_place(self):
        key = "never_ask_for_this_key"
        self.assertTrue(has_reboot_took_place(key))

    def test_reboot_did_not_take_place(self):
        key = "always_ask_for_this_key"
        ask_for_reboot(key)
        self.assertFalse(has_reboot_took_place(key))

    def test_reboot_took_place__uptime_is_lower_than_before(self):
        key = random_string(6)
        ask_for_reboot(key)
        request = Request(key)
        request.make_request()
        request.uptime-=2
        self.assertTrue(request.has_taken_place())

    def test_reboot_took_place__uptime_is_higher_than_before(self):
        key = random_string(6)
        ask_for_reboot(key)
        request = Request(key)
        request.make_request()
        request.uptime+=2
        self.assertFalse(request.has_taken_place())


