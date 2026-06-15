import pytest

from ee_pcb_toolkit.opamps import (
    non_inverting_gain,
    inverting_gain,
    non_inverting_output,
    inverting_output,
    non_inverting_r_feedback_for_gain,
    inverting_r_feedback_for_gain,
    closed_loop_bandwidth,
    required_slew_rate_v_per_us,
)


def test_non_inverting_gain():
    assert non_inverting_gain(r_feedback=10000, r_ground=10000) == pytest.approx(2.0)


def test_inverting_gain():
    assert inverting_gain(r_feedback=10000, r_input=5000) == pytest.approx(2.0)


def test_non_inverting_output():
    assert non_inverting_output(vin=1.0, r_feedback=10000, r_ground=10000) == pytest.approx(2.0)


def test_inverting_output():
    assert inverting_output(vin=1.0, r_feedback=10000, r_input=5000) == pytest.approx(-2.0)


def test_non_inverting_r_feedback_for_gain():
    assert non_inverting_r_feedback_for_gain(target_gain=3.0, r_ground=10000) == pytest.approx(20000)


def test_inverting_r_feedback_for_gain():
    assert inverting_r_feedback_for_gain(target_gain=2.0, r_input=10000) == pytest.approx(20000)


def test_closed_loop_bandwidth():
    assert closed_loop_bandwidth(gain_bandwidth_hz=1_000_000, closed_loop_gain=10) == pytest.approx(100_000)


def test_required_slew_rate_v_per_us():
    assert required_slew_rate_v_per_us(v_peak=1.0, frequency_hz=100_000) == pytest.approx(0.628318, rel=1e-5)


def test_non_inverting_gain_less_than_one_raises_error():
    with pytest.raises(ValueError):
        non_inverting_r_feedback_for_gain(target_gain=0.5, r_ground=10000)
