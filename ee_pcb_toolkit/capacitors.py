###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: capacitors.py
###################################################################################################################################

"""
Capacitor, RC filter, and capacitor impedance calculations.
"""

import math


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def rc_time_constant(r_ohms: float, c_farads: float) -> float:
    """Calculate RC time constant in seconds."""
    _validate_positive(r_ohms, "Resistance")
    _validate_positive(c_farads, "Capacitance")

    return r_ohms * c_farads


def rc_cutoff_frequency(r_ohms: float, c_farads: float) -> float:
    """Calculate RC low-pass or high-pass cutoff frequency in Hz."""
    _validate_positive(r_ohms, "Resistance")
    _validate_positive(c_farads, "Capacitance")

    return 1 / (2 * math.pi * r_ohms * c_farads)


def capacitor_reactance(frequency_hz: float, c_farads: float) -> float:
    """Calculate ideal capacitor reactance in ohms."""
    _validate_positive(frequency_hz, "Frequency")
    _validate_positive(c_farads, "Capacitance")

    return 1 / (2 * math.pi * frequency_hz * c_farads)
