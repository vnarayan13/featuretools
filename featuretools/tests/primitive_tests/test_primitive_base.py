from datetime import datetime

import pandas as pd

from featuretools.primitives import IsNull, Max
from featuretools.primitives.base import TransformPrimitive, make_agg_primitive
from featuretools.variable_types import DatetimeTimeIndex, Numeric, TimeSinceLast


def test_call_agg():
    primitive = Max()

    # the assert is run twice on purpose
    assert 5 == primitive(range(6))
    assert 5 == primitive(range(6))


def test_call_trans():
    primitive = IsNull()
    assert pd.Series([False for i in range(6)]).equals(primitive(range(6)))
    assert pd.Series([False for i in range(6)]).equals(primitive(range(6)))


def test_uses_calc_time():
    primitive = TimeSinceLast()
    datetimes = pd.Series([datetime(2015, 6, 7), datetime(2015, 6, 6)])
    answer = 86400.0
    assert answer == primitive(datetimes, time=datetime(2015, 6, 8))


def test_call_multiple_args():
    class TestPrimitive(TransformPrimitive):
        def get_function(self):
            def test(x, y):
                return y
            return test
    primitive = TestPrimitive()
    assert pd.Series([0, 1]).equals(primitive(range(1), range(2)))
    assert pd.Series([0, 1]).equals(primitive(range(1), range(2)))


def test_get_function_called_once():
    class TestPrimitive(TransformPrimitive):
        def __init__(self):
            self.get_function_call_count = 0

        def get_function(self):
            self.get_function_call_count += 1

            def test(x):
                return x
            return test

    primitive = TestPrimitive()
    primitive(range(6))
    primitive(range(6))
    assert primitive.get_function_call_count == 1