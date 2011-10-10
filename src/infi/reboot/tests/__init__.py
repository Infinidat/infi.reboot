__import__("pkg_resources").declare_namespace(__name__)

import os
import unittest
import logging
from .. make_request, has_reboot_took_place, Request

def random_string(length):
    import random
    import string #pylint: disable-msg=W0402

    char_set = string.ascii_uppercase + string.digits
    return ''.join(random.sample(char_set, length))

class RequestTest(unittest.TestCase):
    def test_get_time(self):
        request = Request(None)
        self.assertIsInstance(request.get_current_time(), int)

    def test_get_uptime(self):
        request = Request(None)
        self.assertLess(request.get_current_uptime(), request.get_current_time())

    def test_request_works(self):
        random_key = random_string(6)
        request = Request(random_key)
        logging.debug("reboot key file is {!r}".format(request._get_key_filepath()))
        self.assertFalse(request.has_taken_place())
        reqeust.make_request()
        self.assertFalse(request.has_taken_place())
        request._remove_key_file()
        self.assertTrue(request.has_taken_place())

class RequestMockTest(unittest.TestCase):
    def test_reboot_did_not_take_place(self):
        raise NotImplementedError()

    def test_reboot_took_place__uptime_is_lower_than_before(self):
        raise NotImplementedError()

    def test_reboot_took_place__uptime_is_higher_than_before(self):
        raise NotImplementedError()
    
