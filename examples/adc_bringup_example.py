###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: adc_bringup_example.py
###################################################################################################################################

"""
Example: ADC bring-up calculations.

Scenario:
A 0-10 V sensor needs to be read by a 12-bit ADC with a 3.3 V reference.

We want to calculate:
1. ADC LSB size
2. Resistor divider values for scaling 10 V down to 3.3 V
3. Expected ADC code for a 5 V sensor input
"""

from ee_pcb_toolkit.adc import (
    adc_lsb_size,
    adc_divider_r_top,
    adc_divider_output,
    sensor_voltage_to_adc_code,
)


# ADC inputs
v_ref = 3.3
resolution_bits = 12

# Sensor/interface inputs
sensor_vmax = 10.0
adc_vmax = 3.3
r_bottom = 10000

# Example sensor voltage during bring-up
sensor_voltage = 5.0


lsb = adc_lsb_size(
    v_ref=v_ref,
    resolution_bits=resolution_bits,
)

r_top = adc_divider_r_top(
    vin_max=sensor_vmax,
    adc_vmax=adc_vmax,
    r_bottom=r_bottom,
)

adc_input_voltage = adc_divider_output(
    vin=sensor_voltage,
    r_top=r_top,
    r_bottom=r_bottom,
)

adc_code = sensor_voltage_to_adc_code(
    sensor_voltage_v=sensor_voltage,
    r_top=r_top,
    r_bottom=r_bottom,
    v_ref=v_ref,
    resolution_bits=resolution_bits,
)


print("ADC Bring-Up Example")
print("--------------------")
print(f"ADC reference voltage: {v_ref:.2f} V")
print(f"ADC resolution: {resolution_bits} bits")
print(f"ADC LSB size: {lsb:.6f} V/count")
print()
print(f"Sensor maximum voltage: {sensor_vmax:.2f} V")
print(f"ADC maximum input voltage: {adc_vmax:.2f} V")
print(f"Bottom resistor: {r_bottom:.1f} ohms")
print(f"Calculated top resistor: {r_top:.1f} ohms")
print()
print(f"Sensor voltage during test: {sensor_voltage:.2f} V")
print(f"ADC input voltage after divider: {adc_input_voltage:.4f} V")
print(f"Expected ADC code: {adc_code}")
