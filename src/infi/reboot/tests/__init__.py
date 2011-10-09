__import__("pkg_resources").declare_namespace(__name__)

import unittest

from .. make_request, has_reboot_took_place, Request
class RequestTest(unittest.TestCase):
    def test_time(self):
        request = Request(None)
        self.assertIsInstance(request.get_current_time(), int)

    def test_uptime(self):
        request = Request(None)
        self.assertLess(request.get_current_uptime(), request.get_current_time())
    
