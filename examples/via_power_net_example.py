###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: via_power_net_example.py
###################################################################################################################################

"""
Example: Via planning for a PCB power net.

Scenario:
A 3.3 V rail needs to move from one PCB layer to another through vias.
The rail carries 2 A.

We want to estimate:
1. The resistance of one via
2. How many vias to use
3. The equivalent resistance of the via array
4. The voltage drop through the via array
5. The power loss in the via array
"""

from ee_pcb_toolkit.vias import (
    via_barrel_resistance,
    vias_needed,
    via_array_equivalent_resistance,
    via_voltage_drop,
    via_power_loss,
)


# Design inputs
rail_voltage_v = 3.3
total_current_a = 2.0

board_thickness_mm = 1.6
finished_hole_diameter_mm = 0.3
plating_thickness_um = 25.0

# Conservative design assumption
allowed_current_per_via_a = 0.5


# Calculations
single_via_resistance_ohms = via_barrel_resistance(
    board_thickness_mm=board_thickness_mm,
    finished_hole_diameter_mm=finished_hole_diameter_mm,
    plating_thickness_um=plating_thickness_um,
)

number_of_vias = vias_needed(
    total_current_a=total_current_a,
    current_per_via_a=allowed_current_per_via_a,
)

via_array_resistance_ohms = via_array_equivalent_resistance(
    single_via_resistance_ohms=single_via_resistance_ohms,
    number_of_vias=number_of_vias,
)

voltage_drop_v = via_voltage_drop(
    current_a=total_current_a,
    via_resistance_ohms=via_array_resistance_ohms,
)

power_loss_w = via_power_loss(
    current_a=total_current_a,
    via_resistance_ohms=via_array_resistance_ohms,
)


# Results
print("Via Power Net Example")
print("---------------------")
print(f"Rail voltage: {rail_voltage_v:.2f} V")
print(f"Total current: {total_current_a:.2f} A")
print()
print(f"Board thickness: {board_thickness_mm:.2f} mm")
print(f"Finished via hole diameter: {finished_hole_diameter_mm:.2f} mm")
print(f"Via plating thickness: {plating_thickness_um:.1f} um")
print()
print(f"Single via resistance: {single_via_resistance_ohms:.6f} ohms")
print(f"Allowed current per via: {allowed_current_per_via_a:.2f} A")
print(f"Recommended number of vias: {number_of_vias}")
print(f"Via array resistance: {via_array_resistance_ohms:.6f} ohms")
print()
print(f"Voltage drop through via array: {voltage_drop_v:.6f} V")
print(f"Power loss in via array: {power_loss_w:.6f} W")
