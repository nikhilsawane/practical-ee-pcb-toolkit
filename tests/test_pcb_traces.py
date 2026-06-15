import pytest

from ee_pcb_toolkit.pcb_traces import trace_resistance, trace_voltage_drop, trace_power_loss


def test_trace_resistance_positive():
    assert trace_resistance(length_mm=100, width_mm=0.25, copper_oz=1.0) > 0


def test_trace_voltage_drop():
    assert trace_voltage_drop(current_a=2.0, resistance_ohms=0.1) == pytest.approx(0.2)


def test_trace_power_loss():
    assert trace_power_loss(current_a=2.0, resistance_ohms=0.1) == pytest.approx(0.4)
