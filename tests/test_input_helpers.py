import pytest

from ee_pcb_toolkit.input_helpers import (
    parse_engineering_value,
    LENGTH_TO_MM,
    RESISTANCE_TO_OHMS,
    CAPACITANCE_TO_FARADS,
    CURRENT_TO_AMPS,
    VOLTAGE_TO_VOLTS,
    FREQUENCY_TO_HZ,
)


def test_parse_length_mil_to_mm():
    assert parse_engineering_value("22 mil", LENGTH_TO_MM, "mm") == pytest.approx(0.5588)


def test_parse_length_default_mm():
    assert parse_engineering_value("10", LENGTH_TO_MM, "mm") == pytest.approx(10)


def test_parse_resistance_k():
    assert parse_engineering_value("4.7k", RESISTANCE_TO_OHMS, "ohm") == pytest.approx(4700)


def test_parse_capacitance_nf():
    assert parse_engineering_value("100 nF", CAPACITANCE_TO_FARADS, "f") == pytest.approx(100e-9)


def test_parse_current_ma():
    assert parse_engineering_value("500 mA", CURRENT_TO_AMPS, "a") == pytest.approx(0.5)


def test_parse_voltage_mv():
    assert parse_engineering_value("3300 mV", VOLTAGE_TO_VOLTS, "v") == pytest.approx(3.3)


def test_parse_frequency_khz():
    assert parse_engineering_value("10 kHz", FREQUENCY_TO_HZ, "hz") == pytest.approx(10000)


def test_invalid_unit_raises_error():
    with pytest.raises(ValueError):
        parse_engineering_value("10 banana", LENGTH_TO_MM, "mm")
