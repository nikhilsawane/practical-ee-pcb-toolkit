###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: standard_values.py
###################################################################################################################################

"""
Standard resistor and capacitor value selection helpers.

Supports common E-series preferred values:
E3, E6, E12, E24, E48, and E96.

Useful for:
- selecting nearest real resistor values
- selecting nearest real capacitor values
- finding lower/higher preferred values
- checking percent error from target values
"""

import math


E_SERIES_COUNTS = {
    "E3": 3,
    "E6": 6,
    "E12": 12,
    "E24": 24,
    "E48": 48,
    "E96": 96,
}

E_SERIES_BASE_VALUES = {
    "E3": [1.0, 2.2, 4.7],
    "E6": [1.0, 1.5, 2.2, 3.3, 4.7, 6.8],
    "E12": [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2],
    "E24": [
        1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0,
        2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3,
        4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1,
    ],
}


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def _normalize_series(series: str) -> str:
    normalized = series.strip().upper()

    if normalized not in E_SERIES_COUNTS:
        valid = ", ".join(E_SERIES_COUNTS.keys())
        raise ValueError(f"Unsupported E-series '{series}'. Valid options: {valid}")

    return normalized


def _round_significant(value: float, digits: int) -> float:
    if value == 0:
        return 0.0

    return round(value, digits - int(math.floor(math.log10(abs(value)))) - 1)


def e_series_base_values(series: str) -> list[float]:
    """
    Return one decade of E-series base values.

    Values are normalized between 1.0 and 10.0.
    """
    normalized = _normalize_series(series)

    if normalized in E_SERIES_BASE_VALUES:
        return E_SERIES_BASE_VALUES[normalized]

    count = E_SERIES_COUNTS[normalized]

    if normalized == "E48":
        digits = 2
    else:
        digits = 3

    values = []

    for index in range(count):
        value = 10 ** (index / count)
        values.append(_round_significant(value, digits))

    return sorted(set(values))


def standard_values_in_range(
    min_value: float,
    max_value: float,
    series: str = "E24",
) -> list[float]:
    """Generate standard values between min_value and max_value."""
    _validate_positive(min_value, "Minimum value")
    _validate_positive(max_value, "Maximum value")

    if min_value > max_value:
        raise ValueError("Minimum value cannot be greater than maximum value.")

    base_values = e_series_base_values(series)

    min_decade = math.floor(math.log10(min_value)) - 1
    max_decade = math.ceil(math.log10(max_value)) + 1

    values = []

    for decade in range(min_decade, max_decade + 1):
        multiplier = 10 ** decade

        for base in base_values:
            candidate = base * multiplier

            if min_value <= candidate <= max_value:
                values.append(candidate)

    return sorted(set(values))


def nearest_standard_value(
    target_value: float,
    series: str = "E24",
) -> dict[str, float | str]:
    """Find the nearest standard E-series value."""
    _validate_positive(target_value, "Target value")

    candidates = standard_values_in_range(
        min_value=target_value / 10,
        max_value=target_value * 10,
        series=series,
    )

    nearest = min(candidates, key=lambda value: abs(value - target_value))

    error = nearest - target_value
    error_percent = (error / target_value) * 100

    return {
        "series": _normalize_series(series),
        "target_value": target_value,
        "nearest_value": nearest,
        "error": error,
        "error_percent": error_percent,
    }


def next_lower_standard_value(
    target_value: float,
    series: str = "E24",
) -> float:
    """Find the nearest standard value less than or equal to target_value."""
    _validate_positive(target_value, "Target value")

    candidates = standard_values_in_range(
        min_value=target_value / 10,
        max_value=target_value,
        series=series,
    )

    return max(candidates)


def next_higher_standard_value(
    target_value: float,
    series: str = "E24",
) -> float:
    """Find the nearest standard value greater than or equal to target_value."""
    _validate_positive(target_value, "Target value")

    candidates = standard_values_in_range(
        min_value=target_value,
        max_value=target_value * 10,
        series=series,
    )

    return min(candidates)


def bracket_standard_values(
    target_value: float,
    series: str = "E24",
) -> dict[str, float | str]:
    """Return lower, nearest, and higher standard values."""
    nearest = nearest_standard_value(
        target_value=target_value,
        series=series,
    )

    lower = next_lower_standard_value(
        target_value=target_value,
        series=series,
    )

    higher = next_higher_standard_value(
        target_value=target_value,
        series=series,
    )

    return {
        "series": _normalize_series(series),
        "target_value": target_value,
        "lower_value": lower,
        "nearest_value": nearest["nearest_value"],
        "higher_value": higher,
        "nearest_error_percent": nearest["error_percent"],
    }


def format_ohms(value_ohms: float) -> str:
    """Format a resistance value in engineering-friendly units."""
    _validate_positive(value_ohms, "Resistance")

    if value_ohms >= 1_000_000:
        return f"{value_ohms / 1_000_000:.4g} Mohm"

    if value_ohms >= 1_000:
        return f"{value_ohms / 1_000:.4g} kohm"

    return f"{value_ohms:.4g} ohm"


def format_farads(value_farads: float) -> str:
    """Format a capacitance value in engineering-friendly units."""
    _validate_positive(value_farads, "Capacitance")

    if value_farads >= 1e-3:
        return f"{value_farads * 1e3:.4g} mF"

    if value_farads >= 1e-6:
        return f"{value_farads * 1e6:.4g} uF"

    if value_farads >= 1e-9:
        return f"{value_farads * 1e9:.4g} nF"

    if value_farads >= 1e-12:
        return f"{value_farads * 1e12:.4g} pF"

    return f"{value_farads:.4g} F"
