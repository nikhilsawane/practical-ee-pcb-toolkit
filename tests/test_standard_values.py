import pytest

from ee_pcb_toolkit.standard_values import (
    e_series_base_values,
    standard_values_in_range,
    nearest_standard_value,
    next_lower_standard_value,
    next_higher_standard_value,
    bracket_standard_values,
    format_ohms,
    format_farads,
)


def test_e24_base_values_count():
    assert len(e_series_base_values("E24")) == 24


def test_standard_values_in_range_e12():
    values = standard_values_in_range(
        min_value=1000,
        max_value=10000,
        series="E12",
    )

    assert 1000 in values
    assert 8200 in values


def test_nearest_e24_resistor_value():
    result = nearest_standard_value(
        target_value=31_250,
        series="E24",
    )

    assert result["nearest_value"] == pytest.approx(30_000)
    assert result["error_percent"] == pytest.approx(-4.0)


def test_lower_e24_resistor_value():
    assert next_lower_standard_value(
        target_value=31_250,
        series="E24",
    ) == pytest.approx(30_000)


def test_higher_e24_resistor_value():
    assert next_higher_standard_value(
        target_value=31_250,
        series="E24",
    ) == pytest.approx(33_000)


def test_bracket_standard_values():
    result = bracket_standard_values(
        target_value=31_250,
        series="E24",
    )

    assert result["lower_value"] == pytest.approx(30_000)
    assert result["nearest_value"] == pytest.approx(30_000)
    assert result["higher_value"] == pytest.approx(33_000)


def test_nearest_e24_capacitor_value():
    result = nearest_standard_value(
        target_value=15.9e-9,
        series="E24",
    )

    assert result["nearest_value"] == pytest.approx(16e-9)


def test_format_ohms_kohm():
    assert format_ohms(33000) == "33 kohm"


def test_format_farads_nf():
    assert format_farads(16e-9) == "16 nF"


def test_invalid_series_raises_error():
    with pytest.raises(ValueError):
        nearest_standard_value(
            target_value=1000,
            series="E99",
        )

