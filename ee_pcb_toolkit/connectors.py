###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: connectors.py
###################################################################################################################################

"""
Connector helper calculations.

These functions are useful for connector current planning, pin derating,
parallel power pins, contact resistance checks, voltage drop estimates,
and connector power loss estimates.
"""

import math


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def _validate_pin_count(number_of_pins: int) -> None:
    if number_of_pins <= 0:
        raise ValueError("Number of pins must be greater than zero.")


def _validate_derating_factor(derating_factor: float) -> None:
    if derating_factor <= 0 or derating_factor > 1:
        raise ValueError("Derating factor must be greater than 0 and less than or equal to 1.")


def derated_current_per_pin(rated_current_per_pin_a: float, derating_factor: float = 1.0) -> float:
    """Calculate derated allowable current per connector pin."""
    _validate_positive(rated_current_per_pin_a, "Rated current per pin")
    _validate_derating_factor(derating_factor)

    return rated_current_per_pin_a * derating_factor


def connector_total_current_capacity(
    number_of_pins: int,
    rated_current_per_pin_a: float,
    derating_factor: float = 1.0,
) -> float:
    """Calculate total derated current capacity for parallel connector pins."""
    _validate_pin_count(number_of_pins)

    return number_of_pins * derated_current_per_pin(
        rated_current_per_pin_a=rated_current_per_pin_a,
        derating_factor=derating_factor,
    )


def pins_needed_for_current(
    total_current_a: float,
    rated_current_per_pin_a: float,
    derating_factor: float = 1.0,
) -> int:
    """Calculate the number of parallel connector pins needed for a current path."""
    _validate_positive(total_current_a, "Total current")

    allowed_current_per_pin = derated_current_per_pin(
        rated_current_per_pin_a=rated_current_per_pin_a,
        derating_factor=derating_factor,
    )

    return math.ceil(total_current_a / allowed_current_per_pin)


def current_per_pin(total_current_a: float, number_of_pins: int) -> float:
    """Calculate current carried by each parallel connector pin."""
    _validate_positive(total_current_a, "Total current")
    _validate_pin_count(number_of_pins)

    return total_current_a / number_of_pins


def contact_resistance_ohms(contact_resistance_mohm: float) -> float:
    """Convert contact resistance from milliohms to ohms."""
    _validate_positive(contact_resistance_mohm, "Contact resistance")

    return contact_resistance_mohm / 1000


def equivalent_parallel_contact_resistance(
    contact_resistance_mohm: float,
    number_of_parallel_pins: int,
) -> float:
    """Calculate equivalent resistance for identical contacts in parallel."""
    _validate_pin_count(number_of_parallel_pins)

    single_contact_resistance = contact_resistance_ohms(contact_resistance_mohm)

    return single_contact_resistance / number_of_parallel_pins


def connector_voltage_drop(
    total_current_a: float,
    contact_resistance_mohm: float,
    number_of_parallel_pins: int = 1,
) -> float:
    """Calculate voltage drop through parallel connector contacts."""
    _validate_positive(total_current_a, "Total current")

    equivalent_resistance = equivalent_parallel_contact_resistance(
        contact_resistance_mohm=contact_resistance_mohm,
        number_of_parallel_pins=number_of_parallel_pins,
    )

    return total_current_a * equivalent_resistance


def connector_power_loss(
    total_current_a: float,
    contact_resistance_mohm: float,
    number_of_parallel_pins: int = 1,
) -> float:
    """Calculate power loss through parallel connector contacts."""
    _validate_positive(total_current_a, "Total current")

    equivalent_resistance = equivalent_parallel_contact_resistance(
        contact_resistance_mohm=contact_resistance_mohm,
        number_of_parallel_pins=number_of_parallel_pins,
    )

    return total_current_a**2 * equivalent_resistance


def is_current_within_connector_rating(
    total_current_a: float,
    number_of_pins: int,
    rated_current_per_pin_a: float,
    derating_factor: float = 1.0,
) -> bool:
    """Check whether the total current is within the derated connector pin rating."""
    capacity = connector_total_current_capacity(
        number_of_pins=number_of_pins,
        rated_current_per_pin_a=rated_current_per_pin_a,
        derating_factor=derating_factor,
    )

    return total_current_a <= capacity
