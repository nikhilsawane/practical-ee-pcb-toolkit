###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: opamp_front_end_example.py
###################################################################################################################################

"""
Example: Op-amp front-end calculation.

Scenario:
A sensor outputs 0.5 V, but the ADC range is 0-3.3 V.
We want to amplify the signal before feeding it into the ADC.

This example calculates:
1. Non-inverting amplifier gain
2. Output voltage
3. Estimated closed-loop bandwidth
4. Required slew rate
"""

from ee_pcb_toolkit.opamps import (
    non_inverting_gain,
    non_inverting_output,
    closed_loop_bandwidth,
    required_slew_rate_v_per_us,
)


vin = 0.5
r_feedback = 56000
r_ground = 10000

opamp_gain_bandwidth = 1_000_000
signal_frequency = 10_000


gain = non_inverting_gain(
    r_feedback=r_feedback,
    r_ground=r_ground,
)

vout = non_inverting_output(
    vin=vin,
    r_feedback=r_feedback,
    r_ground=r_ground,
)

bandwidth = closed_loop_bandwidth(
    gain_bandwidth_hz=opamp_gain_bandwidth,
    closed_loop_gain=gain,
)

slew_rate = required_slew_rate_v_per_us(
    v_peak=vout,
    frequency_hz=signal_frequency,
)


print("Op-Amp Front-End Example")
print("------------------------")
print(f"Input voltage: {vin:.3f} V")
print(f"Feedback resistor: {r_feedback:.1f} ohms")
print(f"Ground resistor: {r_ground:.1f} ohms")
print()
print(f"Non-inverting gain: {gain:.3f}")
print(f"Output voltage: {vout:.3f} V")
print()
print(f"Op-amp gain-bandwidth product: {opamp_gain_bandwidth:.1f} Hz")
print(f"Estimated closed-loop bandwidth: {bandwidth:.1f} Hz")
print(f"Required slew rate: {slew_rate:.6f} V/us")
