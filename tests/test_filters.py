import pytest

from ee_pcb_toolkit.filters import (
    rc_cutoff_frequency,
    rc_resistance_for_cutoff,
    rc_capacitance_for_cutoff,
    first_order_lowpass_gain,
    first_order_highpass_gain,
    lowpass_output_voltage,
    highpass_output_voltage,
    gain_to_db,
    db_to_gain,
)


def test_rc_cutoff_frequency():
    assert rc_cutoff_frequency(r_ohms=10000, c_farads=100e-9) == pytest.approx(159.154943, rel=1e-6)


def test_rc_resistance_for_cutoff():
    assert rc_resistance_for_cutoff(cutoff_hz=159.154943, c_farads=100e-9) == pytest.approx(10000, rel=1e-6)


def test_rc_capacitance_for_cutoff():
    assert rc_capacitance_for_cutoff(cutoff_hz=159.154943, r_ohms=10000) == pytest.approx(100e-9, rel=1e-6)


def test_lowpass_gain_at_cutoff():
    assert first_order_lowpass_gain(frequency_hz=1000, cutoff_hz=1000) == pytest.approx(0.70710678)


def test_highpass_gain_at_cutoff():
    assert first_order_highpass_gain(frequency_hz=1000, cutoff_hz=1000) == pytest.approx(0.70710678)


def test_lowpass_output_voltage():
    assert lowpass_output_voltage(vin=1.0, frequency_hz=1000, cutoff_hz=1000) == pytest.approx(0.70710678)


def test_highpass_output_voltage():
    assert highpass_output_voltage(vin=1.0, frequency_hz=1000, cutoff_hz=1000) == pytest.approx(0.70710678)


def test_gain_to_db_unity():
    assert gain_to_db(1.0) == pytest.approx(0.0)


def test_gain_to_db_half():
    assert gain_to_db(0.5) == pytest.approx(-6.0205999)


def test_db_to_gain_minus_6db():
    assert db_to_gain(-6.0205999) == pytest.approx(0.5)
