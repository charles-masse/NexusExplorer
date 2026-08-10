import pytest


def test_sum():
    assert (1 + 1) == pytest.approx(2)