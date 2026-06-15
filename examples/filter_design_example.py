###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: filter_design_example.py
###################################################################################################################################

"""
Example: RC filter design and response check.

Scenario:
A sensor signal is going into an ADC input. We want to add a simple RC low-pass
filter around 1 kHz to reduce high-frequency noise.

This example calculates:
1. Cutoff frequency from R and C
2. Required resistor for a target cutoff
3. Low-pass gain at a test frequency
4. Output voltage at that frequency
5. Gain in dB
"""

from ee_pcb_toolkit.filters import (
    rc_cutoff_frequency,
    rc_resistance_for_cutoff,
    first_order_lowpass_gain,
    lowpass_output_voltage,
    gain_to_db,
)


# Existing RC values
r_ohms = 1000
c_farads = 100e-9

# Target filter design
target_cutoff_hz = 1000
chosen_capacitor_f = 100e-9

# Response check
signal_frequency_hz = 5000
input_voltage_v = 1.0


actual_cutoff = rc_cutoff_frequency(
    r_ohms=r_ohms,
    c_farads=c_farads,
)

required_resistor = rc_resistance_for_cutoff(
    cutoff_hz=target_cutoff_hz,
    c_farads=chosen_capacitor_f,
)

lowpass_gain = first_order_lowpass_gain(
    frequency_hz=signal_frequency_hz,
    cutoff_hz=target_cutoff_hz,
)

output_voltage = lowpass_output_voltage(
    vin=input_voltage_v,
    frequency_hz=signal_frequency_hz,
    cutoff_hz=target_cutoff_hz,
)

gain_db = gain_to_db(lowpass_gain)


print("RC Filter Design Example")
print("------------------------")
print(f"Existing resistor: {r_ohms:.1f} ohms")
print(f"Existing capacitor: {c_farads:.9f} F")
print(f"Actual cutoff frequency: {actual_cutoff:.2f} Hz")
print()
print(f"Target cutoff frequency: {target_cutoff_hz:.2f} Hz")
print(f"Chosen capacitor: {chosen_capacitor_f:.9f} F")
print(f"Required resistor: {required_resistor:.2f} ohms")
print()
print(f"Input voltage: {input_voltage_v:.3f} V")
print(f"Signal frequency: {signal_frequency_hz:.2f} Hz")
print(f"Low-pass gain: {lowpass_gain:.6f}")
print(f"Low-pass gain: {gain_db:.2f} dB")
print(f"Output voltage: {output_voltage:.6f} V")
