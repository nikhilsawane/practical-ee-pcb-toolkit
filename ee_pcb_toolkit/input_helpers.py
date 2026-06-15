###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: input_helpers.py
###################################################################################################################################

"""
Input parsing helpers for command-line calculators.

These helpers allow engineering-friendly inputs such as:
- 22 mil
- 0.5 mm
- 10k
- 4.7k
- 100 nF
- 10 uF
- 500 mA
"""

import re


LENGTH_TO_MM = {
    "mm": 1.0,
    "millimeter": 1.0,
    "millimeters": 1.0,
    "mil": 0.0254,
    "mils": 0.0254,
    "in": 25.4,
    "inch": 25.4,
    "inches": 25.4,
}

RESISTANCE_TO_OHMS = {
    "": 1.0,
    "r": 1.0,
    "ohm": 1.0,
    "ohms": 1.0,
    "k": 1_000.0,
    "kohm": 1_000.0,
    "kohms": 1_000.0,
    "meg": 1_000_000.0,
    "megohm": 1_000_000.0,
    "megohms": 1_000_000.0,
}

CAPACITANCE_TO_FARADS = {
    "f": 1.0,
    "uf": 1e-6,
    "nf": 1e-9,
    "pf": 1e-12,
}

CURRENT_TO_AMPS = {
    "a": 1.0,
    "amp": 1.0,
    "amps": 1.0,
    "ma": 1e-3,
    "ua": 1e-6,
}

VOLTAGE_TO_VOLTS = {
    "v": 1.0,
    "volt": 1.0,
    "volts": 1.0,
    "mv": 1e-3,
}

PLATING_TO_UM = {
    "um": 1.0,
    "micron": 1.0,
    "microns": 1.0,
    "mm": 1000.0,
}

COPPER_WEIGHT_TO_OZ = {
    "oz": 1.0,
    "ozcu": 1.0,
}


def normalize_unit(unit: str) -> str:
    """Normalize common engineering unit text."""
    return (
        unit.strip()
        .replace("Ω", "ohm")
        .replace("ω", "ohm")
        .replace("µ", "u")
        .replace("μ", "u")
        .replace(" ", "")
        .lower()
    )


def parse_engineering_value(user_input: str, unit_table: dict[str, float], default_unit: str) -> float:
    """
    Parse a value with an optional engineering unit.

    Example:
        parse_engineering_value("22 mil", LENGTH_TO_MM, "mm")
        parse_engineering_value("10k", RESISTANCE_TO_OHMS, "ohm")
        parse_engineering_value("100 nF", CAPACITANCE_TO_FARADS, "f")
    """
    text = user_input.strip()

    pattern = r"^\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*([a-zA-ZµμΩω]*)\s*$"
    match = re.match(pattern, text)

    if not match:
        raise ValueError(f"Could not parse input: {user_input}")

    value = float(match.group(1))
    unit = normalize_unit(match.group(2))

    if unit == "":
        unit = normalize_unit(default_unit)

    if unit not in unit_table:
        valid_units = ", ".join(sorted(unit_table.keys()))
        raise ValueError(f"Unsupported unit '{unit}'. Valid units: {valid_units}")

    return value * unit_table[unit]


def get_engineering_value(
    prompt: str,
    unit_table: dict[str, float],
    default_unit: str,
) -> float:
    """Prompt the user until a valid engineering value is entered."""
    while True:
        user_input = input(prompt).strip()

        try:
            return parse_engineering_value(
                user_input=user_input,
                unit_table=unit_table,
                default_unit=default_unit,
            )
        except ValueError as error:
            print(error)
            print("Please try again.")
