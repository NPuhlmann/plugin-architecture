import unittest
from logging import Logger, DEBUG

from plugins.lower_plugin.lower_plugin import LowerPlugin


class LowerText(unittest.TestCase):

    def testGivenTextIsLowerAfterCall(self):
        erwartet = "hier ist ein text."
        text = "HIER IST EIN TEXT."

        test_logger = Logger("TestLogger", DEBUG)

        plugin = LowerPlugin(logger=test_logger)

        result = plugin.invoke(plugin_name='lower', text=text)
        self.assertEqual(result, erwartet)
