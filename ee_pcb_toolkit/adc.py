###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: adc.py
###################################################################################################################################

"""
ADC helper calculations.

These functions are useful during schematic design, sensor scaling,
embedded bring-up, and hardware debugging.
"""


def _validate_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def _validate_resolution_bits(resolution_bits: int) -> None:
    if resolution_bits <= 0:
        raise ValueError("ADC resolution must be greater than zero bits.")


def adc_max_code(resolution_bits: int) -> int:
    """Calculate the maximum digital output code for an ADC."""
    _validate_resolution_bits(resolution_bits)

    return (2**resolution_bits) - 1


def adc_lsb_size(v_ref: float, resolution_bits: int) -> float:
    """
    Calculate ADC LSB size in volts.

    For an ideal unipolar ADC:
        LSB = Vref / 2^N
    """
    _validate_positive(v_ref, "Reference voltage")
    _validate_resolution_bits(resolution_bits)

    return v_ref / (2**resolution_bits)


def adc_voltage_from_code(code: int, v_ref: float, resolution_bits: int) -> float:
    """Convert an ADC code to the corresponding input voltage estimate."""
    max_code = adc_max_code(resolution_bits)

    if code < 0 or code > max_code:
        raise ValueError(f"ADC code must be between 0 and {max_code}.")

    return code * adc_lsb_size(v_ref=v_ref, resolution_bits=resolution_bits)


def adc_code_from_voltage(voltage_v: float, v_ref: float, resolution_bits: int) -> int:
    """
    Convert an input voltage to the nearest ADC code.

    If voltage equals or exceeds Vref, the output saturates at the maximum ADC code.
    """
    _validate_positive(v_ref, "Reference voltage")
    _validate_resolution_bits(resolution_bits)

    if voltage_v < 0:
        raise ValueError("Input voltage cannot be negative.")

    max_code = adc_max_code(resolution_bits)

    if voltage_v >= v_ref:
        return max_code

    code = round(voltage_v / adc_lsb_size(v_ref=v_ref, resolution_bits=resolution_bits))

    return min(code, max_code)


def adc_percent_full_scale(code: int, resolution_bits: int) -> float:
    """Calculate ADC code as a percent of full scale."""
    max_code = adc_max_code(resolution_bits)

    if code < 0 or code > max_code:
        raise ValueError(f"ADC code must be between 0 and {max_code}.")

    return (code / max_code) * 100


def adc_divider_ratio(vin_max: float, adc_vmax: float) -> float:
    """
    Calculate required divider ratio for scaling a larger signal into an ADC range.

    Example:
        10 V sensor into 3.3 V ADC:
        ratio = 3.3 / 10 = 0.33
    """
    _validate_positive(vin_max, "Maximum input voltage")
    _validate_positive(adc_vmax, "Maximum ADC voltage")

    if adc_vmax > vin_max:
        raise ValueError("ADC maximum voltage should not be greater than input maximum voltage.")

    return adc_vmax / vin_max


def adc_divider_r_top(vin_max: float, adc_vmax: float, r_bottom: float) -> float:
    """
    Calculate the top resistor for an ADC input divider.

    r_top is connected from the input signal to the ADC node.
    r_bottom is connected from the ADC node to ground.
    """
    _validate_positive(r_bottom, "Bottom resistor")

    ratio = adc_divider_ratio(vin_max=vin_max, adc_vmax=adc_vmax)

    return r_bottom * ((1 / ratio) - 1)


def adc_divider_output(vin: float, r_top: float, r_bottom: float) -> float:
    """
    Calculate ADC input voltage after a resistor divider.

    r_top is connected from Vin to the ADC node.
    r_bottom is connected from the ADC node to ground.
    """
    _validate_positive(r_top, "Top resistor")
    _validate_positive(r_bottom, "Bottom resistor")

    return vin * (r_bottom / (r_top + r_bottom))


def sensor_voltage_to_adc_code(
    sensor_voltage_v: float,
    r_top: float,
    r_bottom: float,
    v_ref: float,
    resolution_bits: int,
) -> int:
    """Calculate expected ADC code from a sensor voltage through a resistor divider."""
    adc_input_voltage = adc_divider_output(
        vin=sensor_voltage_v,
        r_top=r_top,
        r_bottom=r_bottom,
    )

    return adc_code_from_voltage(
        voltage_v=adc_input_voltage,
        v_ref=v_ref,
        resolution_bits=resolution_bits,
    )
