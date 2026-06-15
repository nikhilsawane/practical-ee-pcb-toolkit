###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: thermal.py
###################################################################################################################################

"""
Thermal calculations for electronics design.
"""


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def junction_temperature(
    ambient_c: float,
    power_w: float,
    theta_ja_c_per_w: float,
) -> float:
    """Calculate estimated semiconductor junction temperature."""
    _validate_positive(power_w, "Power")
    _validate_positive(theta_ja_c_per_w, "Theta JA")

    return ambient_c + (power_w * theta_ja_c_per_w)


def max_power_for_junction_limit(
    max_junction_c: float,
    ambient_c: float,
    theta_ja_c_per_w: float,
) -> float:
    """Calculate maximum allowed power dissipation for a junction temperature limit."""
    _validate_positive(theta_ja_c_per_w, "Theta JA")

    if max_junction_c <= ambient_c:
        raise ValueError("Maximum junction temperature must be greater than ambient temperature.")

    return (max_junction_c - ambient_c) / theta_ja_c_per_w
