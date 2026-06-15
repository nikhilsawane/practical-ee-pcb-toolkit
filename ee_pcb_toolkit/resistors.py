###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: resistors.py
###################################################################################################################################

"""
Resistor network and voltage divider calculations.
"""


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def series_resistance(*resistors_ohms: float) -> float:
    """Calculate equivalent resistance for resistors in series."""
    for resistor in resistors_ohms:
        _validate_positive(resistor, "Resistance")

    return sum(resistors_ohms)


def parallel_resistance(*resistors_ohms: float) -> float:
    """Calculate equivalent resistance for resistors in parallel."""
    for resistor in resistors_ohms:
        _validate_positive(resistor, "Resistance")

    inverse_sum = sum(1 / resistor for resistor in resistors_ohms)
    return 1 / inverse_sum


def voltage_divider(vin: float, r_top: float, r_bottom: float) -> float:
    """
    Calculate voltage divider output.

    r_top is connected from Vin to Vout.
    r_bottom is connected from Vout to ground.
    """
    _validate_positive(r_top, "Top resistor")
    _validate_positive(r_bottom, "Bottom resistor")

    return vin * (r_bottom / (r_top + r_bottom))


def led_series_resistor(v_supply: float, v_forward: float, current_a: float) -> float:
    """Calculate LED current-limiting resistor."""
    _validate_positive(current_a, "LED current")

    if v_supply <= v_forward:
        raise ValueError("Supply voltage must be greater than LED forward voltage.")

    return (v_supply - v_forward) / current_a
