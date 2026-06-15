###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: signal_integrity.py
###################################################################################################################################

"""
Signal integrity helper calculations.

These are first-pass estimates for PCB timing, edge-rate, wavelength,
and transmission-line checks.
"""

SPEED_OF_LIGHT_M_PER_S = 299_792_458


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def signal_velocity_m_per_s(relative_permittivity: float) -> float:
    """Estimate signal velocity in a PCB dielectric."""
    _validate_positive(relative_permittivity, "Relative permittivity")

    return SPEED_OF_LIGHT_M_PER_S / (relative_permittivity**0.5)


def propagation_delay_ns_per_mm(relative_permittivity: float) -> float:
    """Estimate propagation delay in ns/mm."""
    velocity = signal_velocity_m_per_s(relative_permittivity)

    return (1 / velocity) * 1e9 / 1000


def trace_delay_ns(length_mm: float, relative_permittivity: float) -> float:
    """Estimate signal delay for a PCB trace length."""
    _validate_positive(length_mm, "Trace length")

    return length_mm * propagation_delay_ns_per_mm(relative_permittivity)


def edge_rate_bandwidth_hz(rise_time_s: float) -> float:
    """Estimate bandwidth from signal rise time using BW = 0.35 / rise_time."""
    _validate_positive(rise_time_s, "Rise time")

    return 0.35 / rise_time_s


def wavelength_mm(frequency_hz: float, relative_permittivity: float) -> float:
    """Estimate wavelength in a PCB dielectric."""
    _validate_positive(frequency_hz, "Frequency")

    velocity = signal_velocity_m_per_s(relative_permittivity)

    return (velocity / frequency_hz) * 1000


def quarter_wavelength_mm(frequency_hz: float, relative_permittivity: float) -> float:
    """Estimate quarter wavelength in a PCB dielectric."""
    return wavelength_mm(
        frequency_hz=frequency_hz,
        relative_permittivity=relative_permittivity,
    ) / 4


def lumped_length_limit_mm(
    rise_time_s: float,
    relative_permittivity: float,
    fraction: float = 0.1,
) -> float:
    """
    Estimate max trace length before transmission-line behavior matters.

    Default rule:
    trace delay should be less than 10 percent of rise time.
    """
    _validate_positive(rise_time_s, "Rise time")
    _validate_positive(fraction, "Fraction")

    delay_limit_ns = rise_time_s * 1e9 * fraction
    delay_per_mm = propagation_delay_ns_per_mm(relative_permittivity)

    return delay_limit_ns / delay_per_mm
