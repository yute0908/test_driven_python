import bisect
import collections
from datetime import timedelta
from enum import Enum

PriceEvent = collections.namedtuple("PriceEvent", ["timestamp", "price"])


class StockSignal(Enum):
    buy = 1
    neutral = 0
    sell = -1


class Stock:
    LONG_TERM_TIMESPAN = 10
    SHORT_TERM_TIMESPAN = 5

    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = []

    def update(self, timestamp, price):
        if price < 0:
            raise ValueError("price should not be negative")
        bisect.insort_left(self.price_history, PriceEvent(timestamp, price))

    @property
    def price(self):
        return self.price_history[-1].price if self.price_history else None

    def is_increasing_trend(self):
        return self.price_history[-3].price < self.price_history[-2].price < self.price_history[-1].price

    def get_crossover_signal(self, on_date):
        closing_price_list = []
        NUM_DAYS = self.LONG_TERM_TIMESPAN + 1
        for i in range(NUM_DAYS):
            chk = on_date.date() - timedelta(i)
            for price_event in reversed(self.price_history):
                if price_event.timestamp.date() > chk:
                    pass
                if price_event.timestamp.date() == chk:
                    closing_price_list.insert(0, price_event)
                    break
                if price_event.timestamp.date() < chk:
                    closing_price_list.insert(0, price_event)
                    break

        # Return NEUTRAL signal
        if len(closing_price_list) < NUM_DAYS:
            return StockSignal.neutral

        long_term_series = closing_price_list[-self.LONG_TERM_TIMESPAN:]
        prev_long_term_series = closing_price_list[-self.LONG_TERM_TIMESPAN - 1:-1]
        short_term_series = closing_price_list[-self.SHORT_TERM_TIMESPAN:]
        prev_short_term_series = closing_price_list[-self.SHORT_TERM_TIMESPAN - 1:-1]

        long_term_ma = sum([update.price for update in long_term_series]) / self.LONG_TERM_TIMESPAN
        short_term_ma = sum([update.price for update in short_term_series]) / self.SHORT_TERM_TIMESPAN
        prev_long_term_ma = sum([update.price for update in prev_long_term_series]) / self.LONG_TERM_TIMESPAN
        prev_short_term_ma = sum([update.price for update in prev_short_term_series]) / self.SHORT_TERM_TIMESPAN

        # BUY signal
        if self._is_crossover_below_to_above(prev_short_term_ma, prev_long_term_ma, short_term_ma, long_term_ma):
            return StockSignal.buy

        # SELL signal
        if self._is_crossover_below_to_above(prev_long_term_ma, prev_short_term_ma, long_term_ma, short_term_ma):
            return StockSignal.sell

        # NEUTRAL signal
        return StockSignal.neutral


    def _is_crossover_below_to_above(self, prev_ma, prev_reference_ma, current_ma, current_reference_ma):
        return prev_ma < prev_reference_ma and current_ma > current_reference_ma
