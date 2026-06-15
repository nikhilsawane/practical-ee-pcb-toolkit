###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: opamps.py
###################################################################################################################################

"""
Op-amp helper calculations.

These functions are useful for analog front-end design, sensor signal conditioning,
ADC input scaling, and basic amplifier checks.
"""


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def non_inverting_gain(r_feedback: float, r_ground: float) -> float:
    """
    Calculate gain of a non-inverting amplifier.

    Gain = 1 + Rf / Rg
    """
    _validate_positive(r_feedback, "Feedback resistor")
    _validate_positive(r_ground, "Ground resistor")

    return 1 + (r_feedback / r_ground)


def inverting_gain(r_feedback: float, r_input: float) -> float:
    """
    Calculate gain magnitude of an inverting amplifier.

    Gain magnitude = Rf / Rin
    """
    _validate_positive(r_feedback, "Feedback resistor")
    _validate_positive(r_input, "Input resistor")

    return r_feedback / r_input


def non_inverting_output(vin: float, r_feedback: float, r_ground: float) -> float:
    """Calculate ideal output voltage of a non-inverting amplifier."""
    gain = non_inverting_gain(
        r_feedback=r_feedback,
        r_ground=r_ground,
    )

    return vin * gain


def inverting_output(vin: float, r_feedback: float, r_input: float) -> float:
    """Calculate ideal output voltage of an inverting amplifier."""
    gain = inverting_gain(
        r_feedback=r_feedback,
        r_input=r_input,
    )

    return -vin * gain


def non_inverting_r_feedback_for_gain(target_gain: float, r_ground: float) -> float:
    """
    Calculate required feedback resistor for a target non-inverting gain.

    Rf = Rg * (Gain - 1)
    """
    _validate_positive(target_gain, "Target gain")
    _validate_positive(r_ground, "Ground resistor")

    if target_gain < 1:
        raise ValueError("Non-inverting gain must be at least 1.")

    return r_ground * (target_gain - 1)


def inverting_r_feedback_for_gain(target_gain: float, r_input: float) -> float:
    """
    Calculate required feedback resistor for a target inverting gain magnitude.

    Rf = Gain * Rin
    """
    _validate_positive(target_gain, "Target gain")
    _validate_positive(r_input, "Input resistor")

    return target_gain * r_input


def closed_loop_bandwidth(gain_bandwidth_hz: float, closed_loop_gain: float) -> float:
    """
    Estimate closed-loop bandwidth from op-amp gain-bandwidth product.

    Bandwidth ≈ GBW / Gain
    """
    _validate_positive(gain_bandwidth_hz, "Gain-bandwidth product")
    _validate_positive(closed_loop_gain, "Closed-loop gain")

    return gain_bandwidth_hz / closed_loop_gain


def required_slew_rate(v_peak: float, frequency_hz: float) -> float:
    """
    Calculate required slew rate for a sine wave.

    Slew rate = 2 * pi * f * Vpeak

    Output is in V/s.
    """
    import math

    _validate_positive(v_peak, "Peak voltage")
    _validate_positive(frequency_hz, "Frequency")

    return 2 * math.pi * frequency_hz * v_peak


def required_slew_rate_v_per_us(v_peak: float, frequency_hz: float) -> float:
    """
    Calculate required slew rate for a sine wave.

    Output is in V/us.
    """
    return required_slew_rate(
        v_peak=v_peak,
        frequency_hz=frequency_hz,
    ) / 1_000_000
