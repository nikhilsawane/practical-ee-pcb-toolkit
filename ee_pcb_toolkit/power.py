###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: power.py
###################################################################################################################################

"""
Power electronics and regulator helper calculations.
"""


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def ldo_power_dissipation(vin: float, vout: float, load_current_a: float) -> float:
    """Calculate LDO power dissipation in watts."""
    _validate_positive(load_current_a, "Load current")

    if vin < vout:
        raise ValueError("Input voltage must be greater than or equal to output voltage.")

    return (vin - vout) * load_current_a


def buck_feedback_r_top(vout: float, v_ref: float, r_bottom: float) -> float:
    """Calculate top feedback resistor for an adjustable buck regulator."""
    _validate_positive(vout, "Output voltage")
    _validate_positive(v_ref, "Reference voltage")
    _validate_positive(r_bottom, "Bottom feedback resistor")

    if vout <= v_ref:
        raise ValueError("Output voltage must be greater than reference voltage.")

    return r_bottom * ((vout / v_ref) - 1)


def buck_feedback_r_bottom(vout: float, v_ref: float, r_top: float) -> float:
    """Calculate bottom feedback resistor for an adjustable buck regulator."""
    _validate_positive(vout, "Output voltage")
    _validate_positive(v_ref, "Reference voltage")
    _validate_positive(r_top, "Top feedback resistor")

    if vout <= v_ref:
        raise ValueError("Output voltage must be greater than reference voltage.")

    return r_top / ((vout / v_ref) - 1)


def efficiency_percent(output_power_w: float, input_power_w: float) -> float:
    """Calculate power conversion efficiency in percent."""
    _validate_positive(output_power_w, "Output power")
    _validate_positive(input_power_w, "Input power")

    if output_power_w > input_power_w:
        raise ValueError("Output power cannot be greater than input power.")

    return (output_power_w / input_power_w) * 100


def current_from_power(power_w: float, voltage_v: float) -> float:
    """Calculate current from power and voltage."""
    _validate_positive(power_w, "Power")
    _validate_positive(voltage_v, "Voltage")

    return power_w / voltage_v
