###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: pcb_traces.py
###################################################################################################################################

"""
PCB trace resistance, voltage drop, and power loss calculations.

These are first-order engineering estimates. Final PCB current capacity should be verified using
IPC guidance, manufacturer data, simulation, and lab testing.
"""

from ee_pcb_toolkit.units import copper_oz_to_um

COPPER_RESISTIVITY_OHM_M = 1.724e-8
COPPER_TEMP_COEFF_PER_C = 0.00393


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def trace_cross_section_area_m2(width_mm: float, copper_oz: float = 1.0) -> float:
    """Calculate PCB trace cross-sectional area in square meters."""
    _validate_positive(width_mm, "Trace width")
    _validate_positive(copper_oz, "Copper weight")

    width_m = width_mm / 1000
    thickness_m = copper_oz_to_um(copper_oz) * 1e-6

    return width_m * thickness_m


def trace_resistance(
    length_mm: float,
    width_mm: float,
    copper_oz: float = 1.0,
    temperature_c: float = 20.0,
) -> float:
    """Calculate approximate PCB trace resistance in ohms."""
    _validate_positive(length_mm, "Trace length")
    _validate_positive(width_mm, "Trace width")
    _validate_positive(copper_oz, "Copper weight")

    length_m = length_mm / 1000
    area_m2 = trace_cross_section_area_m2(width_mm, copper_oz)

    adjusted_resistivity = COPPER_RESISTIVITY_OHM_M * (
        1 + COPPER_TEMP_COEFF_PER_C * (temperature_c - 20.0)
    )

    return adjusted_resistivity * length_m / area_m2


def trace_voltage_drop(current_a: float, resistance_ohms: float) -> float:
    """Calculate voltage drop across a PCB trace."""
    _validate_positive(abs(current_a), "Current")
    _validate_positive(resistance_ohms, "Resistance")

    return current_a * resistance_ohms


def trace_power_loss(current_a: float, resistance_ohms: float) -> float:
    """Calculate power loss in a PCB trace."""
    _validate_positive(abs(current_a), "Current")
    _validate_positive(resistance_ohms, "Resistance")

    return current_a**2 * resistance_ohms
