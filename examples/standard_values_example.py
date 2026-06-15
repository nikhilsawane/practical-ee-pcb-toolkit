###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: standard_values_example.py
###################################################################################################################################

"""
Example: Standard resistor and capacitor value selection.
"""

from ee_pcb_toolkit.standard_values import (
    nearest_standard_value,
    bracket_standard_values,
    format_ohms,
    format_farads,
)


target_resistor = 31_250
target_capacitor = 15.9e-9

resistor_result = bracket_standard_values(
    target_value=target_resistor,
    series="E24",
)

capacitor_result = nearest_standard_value(
    target_value=target_capacitor,
    series="E24",
)


print("Standard Values Example")
print("-----------------------")
print()
print("Resistor selection:")
print(f"Target: {format_ohms(target_resistor)}")
print(f"Series: {resistor_result['series']}")
print(f"Lower: {format_ohms(resistor_result['lower_value'])}")
print(f"Nearest: {format_ohms(resistor_result['nearest_value'])}")
print(f"Higher: {format_ohms(resistor_result['higher_value'])}")
print(f"Nearest error: {resistor_result['nearest_error_percent']:.2f}%")
print()
print("Capacitor selection:")
print(f"Target: {format_farads(target_capacitor)}")
print(f"Series: {capacitor_result['series']}")
print(f"Nearest: {format_farads(capacitor_result['nearest_value'])}")
print(f"Nearest error: {capacitor_result['error_percent']:.2f}%")
