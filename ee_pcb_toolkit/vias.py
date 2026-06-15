###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: vias.py
###################################################################################################################################

"""
PCB via calculations.

These functions are first-order estimates for via barrel resistance, voltage drop,
power loss, and via count planning for power nets.

Final via decisions should be verified using PCB manufacturer capabilities,
IPC guidance, simulation, and lab testing.
"""

import math

COPPER_RESISTIVITY_OHM_M = 1.724e-8
COPPER_TEMP_COEFF_PER_C = 0.00393


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def via_barrel_cross_section_area_m2(
    finished_hole_diameter_mm: float,
    plating_thickness_um: float,
) -> float:
    """
    Calculate the copper barrel cross-sectional area of a plated through via.

    The via barrel is modeled as a hollow copper cylinder.
    """
    _validate_positive(finished_hole_diameter_mm, "Finished hole diameter")
    _validate_positive(plating_thickness_um, "Plating thickness")

    inner_radius_m = (finished_hole_diameter_mm / 1000) / 2
    plating_thickness_m = plating_thickness_um * 1e-6
    outer_radius_m = inner_radius_m + plating_thickness_m

    return math.pi * ((outer_radius_m**2) - (inner_radius_m**2))


def via_barrel_resistance(
    board_thickness_mm: float,
    finished_hole_diameter_mm: float,
    plating_thickness_um: float = 25.0,
    temperature_c: float = 20.0,
) -> float:
    """
    Calculate approximate resistance of a plated through via barrel in ohms.

    board_thickness_mm is the via barrel length.
    finished_hole_diameter_mm is the finished drilled/plated hole diameter.
    plating_thickness_um is the copper plating thickness inside the hole.
    """
    _validate_positive(board_thickness_mm, "Board thickness")
    _validate_positive(finished_hole_diameter_mm, "Finished hole diameter")
    _validate_positive(plating_thickness_um, "Plating thickness")

    length_m = board_thickness_mm / 1000
    area_m2 = via_barrel_cross_section_area_m2(
        finished_hole_diameter_mm=finished_hole_diameter_mm,
        plating_thickness_um=plating_thickness_um,
    )

    adjusted_resistivity = COPPER_RESISTIVITY_OHM_M * (
        1 + COPPER_TEMP_COEFF_PER_C * (temperature_c - 20.0)
    )

    return adjusted_resistivity * length_m / area_m2


def via_voltage_drop(current_a: float, via_resistance_ohms: float) -> float:
    """Calculate voltage drop across a via."""
    _validate_positive(abs(current_a), "Current")
    _validate_positive(via_resistance_ohms, "Via resistance")

    return current_a * via_resistance_ohms


def via_power_loss(current_a: float, via_resistance_ohms: float) -> float:
    """Calculate power loss in a via."""
    _validate_positive(abs(current_a), "Current")
    _validate_positive(via_resistance_ohms, "Via resistance")

    return current_a**2 * via_resistance_ohms


def vias_needed(total_current_a: float, current_per_via_a: float) -> int:
    """
    Calculate the minimum number of vias needed for a current path.

    current_per_via_a should come from your design rule, manufacturer guidance,
    conservative engineering judgment, or lab-verified current limit.
    """
    _validate_positive(total_current_a, "Total current")
    _validate_positive(current_per_via_a, "Current per via")

    return math.ceil(total_current_a / current_per_via_a)


def via_array_equivalent_resistance(single_via_resistance_ohms: float, number_of_vias: int) -> float:
    """
    Calculate equivalent resistance for multiple identical vias in parallel.
    """
    _validate_positive(single_via_resistance_ohms, "Single via resistance")

    if number_of_vias <= 0:
        raise ValueError("Number of vias must be greater than zero.")

    return single_via_resistance_ohms / number_of_vias
