import pytest

# We assume math_utils.py has a function called get_average
from math_utils import get_average


def test_integer_average():
    assert get_average([80, 90, 100]) == 90


def test_float_average():
    assert get_average([85, 86]) == 85.5


def test_empty_list():
    # Ensuring the code returns 0 (or handles it) instead of crashing
    assert get_average([]) == 0
