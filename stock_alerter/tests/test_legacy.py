import unittest
from unittest import mock

from stock_alerter.legacy import AlertProcessor


@mock.patch("builtins.print")
class AlertProcessorTest(unittest.TestCase):
    def test_processor_characterization_1(self, mock_print):
        AlertProcessor()
        mock_print.assert_has_calls(
            [mock.call("AAPL", 8), mock.call("GOOG", 15), mock.call("AAPL", 10), mock.call("GOOG", 21)])

    def test_processor_characterization_2(self, mock_print):
        processor = AlertProcessor(autorun=False)
        processor.run()
        mock_print.assert_has_calls(
            [mock.call("AAPL", 8), mock.call("GOOG", 15), mock.call("AAPL", 10), mock.call("GOOG", 21)])
