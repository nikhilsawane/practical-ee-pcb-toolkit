import pytest

from ee_pcb_toolkit.resistors import series_resistance, parallel_resistance, voltage_divider


def test_series_resistance():
    assert series_resistance(100, 200, 300) == pytest.approx(600)


def test_parallel_resistance():
    assert parallel_resistance(100, 100) == pytest.approx(50)


def test_voltage_divider():
    assert voltage_divider(5.0, 10000, 10000) == pytest.approx(2.5)
