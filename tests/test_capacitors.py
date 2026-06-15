import pytest

from ee_pcb_toolkit.capacitors import rc_time_constant, rc_cutoff_frequency


def test_rc_time_constant():
    assert rc_time_constant(1000, 1e-6) == pytest.approx(0.001)


def test_rc_cutoff_frequency():
    assert rc_cutoff_frequency(1000, 1e-6) == pytest.approx(159.154943, rel=1e-6)
