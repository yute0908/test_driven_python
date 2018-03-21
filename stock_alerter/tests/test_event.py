import unittest

from stock_alerter.event import Event


class Mock:

    def __init__(self):
        self.called = False
        self.params = ()

    def __call__(self, *args, **kwargs):
        self.called = True
        self.params = (args, kwargs)


class EventTest(unittest.TestCase):
    def test_a_listener_is_notified_when_an_event_is_raised(self):
        listener = Mock()
        event = Event()
        event.connect(listener)
        event.fire()
        self.assertTrue(listener.called)

    def test_a_listener_is_passed_right_parameters(self):
        listener = Mock()
        event = Event()
        event.connect(listener)
        event.fire(5, shape="square")
        self.assertEqual(((5,), {"shape": "square"}), listener.params)
