###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: filters.py
###################################################################################################################################

"""
Filter helper calculations.

These functions are useful for first-order RC filter design, analog front-end
checks, ADC input filtering, and quick bring-up estimates.
"""

import math


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def rc_cutoff_frequency(r_ohms: float, c_farads: float) -> float:
    """Calculate first-order RC cutoff frequency in Hz."""
    _validate_positive(r_ohms, "Resistance")
    _validate_positive(c_farads, "Capacitance")

    return 1 / (2 * math.pi * r_ohms * c_farads)


def rc_resistance_for_cutoff(cutoff_hz: float, c_farads: float) -> float:
    """Calculate resistor value needed for a target RC cutoff frequency."""
    _validate_positive(cutoff_hz, "Cutoff frequency")
    _validate_positive(c_farads, "Capacitance")

    return 1 / (2 * math.pi * cutoff_hz * c_farads)


def rc_capacitance_for_cutoff(cutoff_hz: float, r_ohms: float) -> float:
    """Calculate capacitor value needed for a target RC cutoff frequency."""
    _validate_positive(cutoff_hz, "Cutoff frequency")
    _validate_positive(r_ohms, "Resistance")

    return 1 / (2 * math.pi * cutoff_hz * r_ohms)


def first_order_lowpass_gain(frequency_hz: float, cutoff_hz: float) -> float:
    """Calculate magnitude gain of a first-order low-pass filter."""
    _validate_positive(frequency_hz, "Frequency")
    _validate_positive(cutoff_hz, "Cutoff frequency")

    ratio = frequency_hz / cutoff_hz
    return 1 / math.sqrt(1 + ratio**2)


def first_order_highpass_gain(frequency_hz: float, cutoff_hz: float) -> float:
    """Calculate magnitude gain of a first-order high-pass filter."""
    _validate_positive(frequency_hz, "Frequency")
    _validate_positive(cutoff_hz, "Cutoff frequency")

    ratio = frequency_hz / cutoff_hz
    return ratio / math.sqrt(1 + ratio**2)


def lowpass_output_voltage(vin: float, frequency_hz: float, cutoff_hz: float) -> float:
    """Calculate first-order low-pass output voltage magnitude."""
    gain = first_order_lowpass_gain(
        frequency_hz=frequency_hz,
        cutoff_hz=cutoff_hz,
    )

    return vin * gain


def highpass_output_voltage(vin: float, frequency_hz: float, cutoff_hz: float) -> float:
    """Calculate first-order high-pass output voltage magnitude."""
    gain = first_order_highpass_gain(
        frequency_hz=frequency_hz,
        cutoff_hz=cutoff_hz,
    )

    return vin * gain


def gain_to_db(gain: float) -> float:
    """Convert voltage gain magnitude to dB."""
    _validate_positive(gain, "Gain")

    return 20 * math.log10(gain)


def db_to_gain(db: float) -> float:
    """Convert dB to voltage gain magnitude."""
    return 10 ** (db / 20)
