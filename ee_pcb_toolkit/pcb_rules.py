###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: pcb_rules.py
###################################################################################################################################

"""
PCB design-rule helper calculations.

This module converts practical Altium-style PCB rules into reusable Python helpers.

Important:
- Current primarily drives trace width.
- Voltage primarily drives clearance.
- These are first-pass engineering estimates and project-rule checks.
"""

import math
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class TraceWidthRule:
    name: str
    min_mil: float
    preferred_mil: float
    max_mil: float
    description: str


@dataclass(frozen=True)
class ViaRule:
    name: str
    pad_diameter_mil: float
    drill_diameter_mil: float
    description: str


@dataclass(frozen=True)
class DiffPairRule:
    name: str
    target_impedance_ohms: float
    width_mil: float
    gap_mil: float
    description: str


TRACE_WIDTH_RULES = {
    "default": TraceWidthRule("Width_default", 8, 8, 12, "Default routing rule for general signals."),
    "power": TraceWidthRule("Width_Power", 8, 12, 16, "General power-net routing rule."),
    "power_input": TraceWidthRule("Width_high_current", 8, 30, 50, "High-current or power-input routing rule."),
    "ntc": TraceWidthRule("Width_NTC_Net", 12, 12, 12, "Fixed-width NTC routing rule."),
    "heater": TraceWidthRule("Width_Heater_Net", 20, 20, 20, "Fixed-width heater routing rule."),
}

VIA_RULES = {
    "default": ViaRule("RoutingVias_Default", 24, 12, "Default routing via rule."),
    "power": ViaRule("RoutingVias_Power", 26, 12, "Power routing via rule."),
    "legacy_default": ViaRule("RoutingVias_default_legacy", 26, 12, "Earlier default via rule."),
    "legacy_power": ViaRule("RoutingVias_Power_legacy", 30, 15, "Earlier power via rule."),
}

DIFF_PAIR_RULES = {
    "diff100_legacy": DiffPairRule("DiffPair100_legacy", 100, 7, 6, "Earlier 100-ohm diff-pair rule: 7 mil width / 6 mil gap."),
    "diff100": DiffPairRule("Diff100", 100, 6, 10, "Current Diff100 rule interpreted as 6 mil width / 10 mil gap."),
    "diff120": DiffPairRule("Diff120", 120, 5, 15, "Current Diff120 rule interpreted as 5 mil width / 15 mil gap."),
}

CLEARANCE_RULES_MIL = {
    "default": 6,
    "digital": 6,
    "plane": 12,
    "board_outline": 10,
    "switching_minimum": 18,
}

COPPER_THICKNESS_MIL_PER_OZ = 1.378


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def copper_thickness_mil(copper_oz: float) -> float:
    """Convert copper weight in oz to approximate copper thickness in mils."""
    _validate_positive(copper_oz, "Copper weight")

    return copper_oz * COPPER_THICKNESS_MIL_PER_OZ


def required_trace_width_mil(
    current_a: float,
    copper_oz: float = 1.0,
    temperature_rise_c: float = 10.0,
    layer: str = "external",
) -> float:
    """
    Estimate required trace width in mils using a common IPC-2221-style approximation.

    Inputs:
        current_a: current through the trace
        copper_oz: copper weight
        temperature_rise_c: allowed temperature rise
        layer: "external" or "internal"

    This is a first-pass estimate, not a final signoff.
    """
    _validate_positive(current_a, "Current")
    _validate_positive(copper_oz, "Copper weight")
    _validate_positive(temperature_rise_c, "Temperature rise")

    layer_normalized = layer.strip().lower()

    if layer_normalized == "external":
        k = 0.048
    elif layer_normalized == "internal":
        k = 0.024
    else:
        raise ValueError("Layer must be either 'external' or 'internal'.")

    area_mil2 = (current_a / (k * (temperature_rise_c**0.44))) ** (1 / 0.725)

    return area_mil2 / copper_thickness_mil(copper_oz)


def get_trace_width_rule(net_class: str) -> TraceWidthRule:
    """Return a trace-width rule by net class."""
    key = net_class.strip().lower()

    if key not in TRACE_WIDTH_RULES:
        valid = ", ".join(sorted(TRACE_WIDTH_RULES.keys()))
        raise ValueError(f"Unknown net class '{net_class}'. Valid options: {valid}")

    return TRACE_WIDTH_RULES[key]


def recommend_trace_width_mil(
    current_a: float,
    net_class: str = "default",
    copper_oz: float = 1.0,
    temperature_rise_c: float = 10.0,
    layer: str = "external",
    preferred_margin: float = 1.25,
) -> dict[str, float | str | bool]:
    """
    Recommend min/preferred/max trace width using current estimate plus LAIR/RADICALS rules.

    The rule max is not silently ignored. If current requires more than the rule max,
    within_rule_max will be False.
    """
    _validate_positive(preferred_margin, "Preferred margin")

    rule = get_trace_width_rule(net_class)

    required_by_current = required_trace_width_mil(
        current_a=current_a,
        copper_oz=copper_oz,
        temperature_rise_c=temperature_rise_c,
        layer=layer,
    )

    calculated_min = max(rule.min_mil, required_by_current)
    calculated_preferred = max(rule.preferred_mil, required_by_current * preferred_margin)

    recommended_preferred = min(calculated_preferred, rule.max_mil)
    within_rule_max = required_by_current <= rule.max_mil

    status = "OK" if within_rule_max else "EXCEEDS_RULE_MAX"

    return {
        "net_class": net_class,
        "rule_name": rule.name,
        "required_by_current_mil": required_by_current,
        "rule_min_mil": rule.min_mil,
        "rule_preferred_mil": rule.preferred_mil,
        "rule_max_mil": rule.max_mil,
        "recommended_min_mil": calculated_min,
        "recommended_preferred_mil": recommended_preferred,
        "recommended_max_mil": rule.max_mil,
        "within_rule_max": within_rule_max,
        "status": status,
    }


def voltage_clearance_recommendation_mil(
    voltage_v: float,
    clearance_type: str = "default",
    trace_width_mil: float | None = None,
) -> dict[str, float | str]:
    """
    Recommend starter clearance in mils.

    LAIR/RADICALS project rules:
        default/digital clearance: 6 mil
        plane clearance: 12 mil
        board outline clearance: 10 mil
        switching clearance: about 3x trace width, usually around 18 mil minimum
    """
    _validate_positive(voltage_v, "Voltage")

    key = clearance_type.strip().lower()

    if key == "switching":
        if trace_width_mil is None:
            base_clearance = CLEARANCE_RULES_MIL["switching_minimum"]
        else:
            _validate_positive(trace_width_mil, "Trace width")
            base_clearance = max(CLEARANCE_RULES_MIL["switching_minimum"], 3 * trace_width_mil)
    else:
        if key not in CLEARANCE_RULES_MIL:
            valid = ", ".join(sorted(CLEARANCE_RULES_MIL.keys()) + ["switching"])
            raise ValueError(f"Unknown clearance type '{clearance_type}'. Valid options: {valid}")
        base_clearance = CLEARANCE_RULES_MIL[key]

    if voltage_v <= 30:
        voltage_based_clearance = base_clearance
    elif voltage_v <= 60:
        voltage_based_clearance = max(base_clearance, 8)
    elif voltage_v <= 150:
        voltage_based_clearance = max(base_clearance, 12)
    elif voltage_v <= 300:
        voltage_based_clearance = max(base_clearance, 20)
    elif voltage_v <= 600:
        voltage_based_clearance = max(base_clearance, 40)
    else:
        voltage_based_clearance = max(base_clearance, 80)

    return {
        "clearance_type": clearance_type,
        "voltage_v": voltage_v,
        "recommended_clearance_mil": voltage_based_clearance,
        "note": "Starter project-rule estimate. Verify against safety, IPC, and manufacturer requirements.",
    }


def via_annular_ring_mil(pad_diameter_mil: float, drill_diameter_mil: float) -> float:
    """Calculate via annular ring in mils."""
    _validate_positive(pad_diameter_mil, "Pad diameter")
    _validate_positive(drill_diameter_mil, "Drill diameter")

    if drill_diameter_mil >= pad_diameter_mil:
        raise ValueError("Drill diameter must be smaller than pad diameter.")

    return (pad_diameter_mil - drill_diameter_mil) / 2


def get_via_rule(rule_name: str) -> ViaRule:
    """Return a via rule."""
    key = rule_name.strip().lower()

    if key not in VIA_RULES:
        valid = ", ".join(sorted(VIA_RULES.keys()))
        raise ValueError(f"Unknown via rule '{rule_name}'. Valid options: {valid}")

    return VIA_RULES[key]


def via_rule_summary(rule_name: str, minimum_annular_ring_mil: float = 6.0) -> dict[str, float | str | bool]:
    """Summarize a via rule and check annular ring."""
    _validate_positive(minimum_annular_ring_mil, "Minimum annular ring")

    rule = get_via_rule(rule_name)
    annular_ring = via_annular_ring_mil(
        pad_diameter_mil=rule.pad_diameter_mil,
        drill_diameter_mil=rule.drill_diameter_mil,
    )

    return {
        "rule_name": rule.name,
        "pad_diameter_mil": rule.pad_diameter_mil,
        "drill_diameter_mil": rule.drill_diameter_mil,
        "annular_ring_mil": annular_ring,
        "minimum_annular_ring_mil": minimum_annular_ring_mil,
        "meets_annular_ring": annular_ring >= minimum_annular_ring_mil,
    }


def get_diff_pair_rule(rule_name: str) -> dict[str, float | str]:
    """Return a differential-pair rule as a dictionary."""
    key = rule_name.strip().lower()

    if key not in DIFF_PAIR_RULES:
        valid = ", ".join(sorted(DIFF_PAIR_RULES.keys()))
        raise ValueError(f"Unknown differential pair rule '{rule_name}'. Valid options: {valid}")

    return asdict(DIFF_PAIR_RULES[key])
