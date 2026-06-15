import pytest

from ee_pcb_toolkit.signal_integrity import (
    signal_velocity_m_per_s,
    propagation_delay_ns_per_mm,
    trace_delay_ns,
    edge_rate_bandwidth_hz,
    wavelength_mm,
    quarter_wavelength_mm,
    lumped_length_limit_mm,
)


def test_signal_velocity_positive():
    assert signal_velocity_m_per_s(relative_permittivity=4.0) > 0


def test_propagation_delay_fr4_approx():
    delay = propagation_delay_ns_per_mm(relative_permittivity=4.0)
    assert delay == pytest.approx(0.006671, rel=1e-3)


def test_trace_delay():
    delay = trace_delay_ns(length_mm=100, relative_permittivity=4.0)
    assert delay == pytest.approx(0.6671, rel=1e-3)


def test_edge_rate_bandwidth():
    bandwidth = edge_rate_bandwidth_hz(rise_time_s=1e-9)
    assert bandwidth == pytest.approx(350_000_000)


def test_wavelength_mm():
    wavelength = wavelength_mm(frequency_hz=1e9, relative_permittivity=4.0)
    assert wavelength == pytest.approx(149.896, rel=1e-3)


def test_quarter_wavelength_mm():
    quarter = quarter_wavelength_mm(frequency_hz=1e9, relative_permittivity=4.0)
    assert quarter == pytest.approx(37.474, rel=1e-3)


def test_lumped_length_limit_mm():
    length = lumped_length_limit_mm(
        rise_time_s=1e-9,
        relative_permittivity=4.0,
        fraction=0.1,
    )

    assert length == pytest.approx(14.9896, rel=1e-3)
