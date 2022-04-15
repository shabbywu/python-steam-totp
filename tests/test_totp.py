import base64
import unittest

from steam_totp import generate_twofactor_code_for_time


class TestSteamTotp(unittest.TestCase):
    def test_generate_twofactor_code_for_time(self):
        cases = [
            ((base64.b64encode(b"foo"), 1024), "TXNN5"),
            ((base64.b64encode(b"foo").decode(), 1024), "TXNN5"),
            ((base64.b64encode(base64.b64encode(b"foo")), 1024), "8XGNF"),
        ]
        for args, expected in cases:
            self.assertEqual(generate_twofactor_code_for_time(*args), expected)
