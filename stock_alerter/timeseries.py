import bisect
import collections
from datetime import timedelta

Update = collections.namedtuple("Update", ["timestamp", "value"])


class TimeSeries:
    def __init__(self):
        self.series = []

    def update(self, timestamp, value):
        bisect.insort_left(self.series, Update(timestamp, value))

    def __getitem__(self, index):
        return self.series[index]

    def get_closing_price_list(self, on_date, num_days):
        closing_price_list = []
        for i in range(num_days):
            chk = on_date.date() - timedelta(i)
            for price_event in reversed(self.series):
                if price_event.timestamp.date() > chk:
                    pass
                if price_event.timestamp.date() == chk:
                    closing_price_list.insert(0, price_event)
                    break
                if price_event.timestamp.date() < chk:
                    closing_price_list.insert(0, price_event)
                    break
        return closing_price_list


class MovingAverage:
    def __init__(self, series, timespan):
        self.series = series
        self.timespan = timespan

    def value_on(self, end_date):
        moving_average_range = self.series.get_closing_price_list(end_date, self.timespan)
        if len(moving_average_range) < self.timespan:
            raise NotEnoughDataException("Not enough data")

        price_list = [item.value for item in moving_average_range]
        return sum(price_list)/len(price_list)


class NotEnoughDataException(Exception):
    pass
