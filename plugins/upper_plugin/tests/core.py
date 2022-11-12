import unittest
from logging import Logger, DEBUG

from plugins.upper_plugin.upper_plugin import UpperPlugin

class UpperText(unittest.TestCase):

    def testGivenTextIsUpperAfterCall(self):
        text = "Hier ist ein Text."
        erwartet = "HIER IST EIN TEXT."

        test_logger = Logger("TestLogger", DEBUG)

        plugin = UpperPlugin(logger=test_logger)

        result = plugin.invoke(plugin_name='upper', text=text)
        self.assertEqual(result, erwartet)
