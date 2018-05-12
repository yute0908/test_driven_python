import unittest

from datetime import datetime

from stock_alerter.timeseries import TimeSeries


class TimeSeriesTest(unittest.TestCase):
    def test_closing_price_list_before_series_start_date(self):
        """
        Empty list is returned if on_date is before the start of the
        series
        The moving average calculation might be done before any data
        has been added to the stock. We return an empty list so that
        the calculation can still proceed as usual.
        """
        series = TimeSeries()
        series.update(datetime(2014, 3, 10), 5)
        on_date = datetime(2014, 3, 9)
        self.assertEqual([], series.get_closing_price_list(on_date, 1))