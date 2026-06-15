###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: units.py
###################################################################################################################################

"""
Unit conversion helpers commonly used in PCB design.
"""

COPPER_OZ_TO_UM = 34.8


def mil_to_mm(mil: float) -> float:
    """Convert mils to millimeters."""
    return mil * 0.0254


def mm_to_mil(mm: float) -> float:
    """Convert millimeters to mils."""
    return mm / 0.0254


def inch_to_mm(inch: float) -> float:
    """Convert inches to millimeters."""
    return inch * 25.4


def mm_to_inch(mm: float) -> float:
    """Convert millimeters to inches."""
    return mm / 25.4


def copper_oz_to_um(copper_oz: float) -> float:
    """Convert copper weight in oz/ft^2 to approximate copper thickness in micrometers."""
    if copper_oz <= 0:
        raise ValueError("Copper weight must be greater than zero.")

    return copper_oz * COPPER_OZ_TO_UM


def um_to_copper_oz(thickness_um: float) -> float:
    """Convert copper thickness in micrometers to approximate copper weight in oz/ft^2."""
    if thickness_um <= 0:
        raise ValueError("Copper thickness must be greater than zero.")

    return thickness_um / COPPER_OZ_TO_UM
