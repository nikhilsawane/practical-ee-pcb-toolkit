###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: connector_power_example.py
###################################################################################################################################

"""
Example: Connector power pin planning.

Scenario:
A 5 V rail carries 6 A through a board-to-board connector.
Each connector pin is rated for 2 A, but we want to derate the rating to 80%.
The contact resistance is estimated as 10 milliohms per contact.

This example calculates:
1. Derated current per pin
2. Number of parallel pins needed
3. Current per pin
4. Connector voltage drop
5. Connector power loss
"""

from ee_pcb_toolkit.connectors import (
    derated_current_per_pin,
    pins_needed_for_current,
    current_per_pin,
    connector_voltage_drop,
    connector_power_loss,
    is_current_within_connector_rating,
)


rail_voltage_v = 5.0
total_current_a = 6.0
rated_current_per_pin_a = 2.0
derating_factor = 0.8
contact_resistance_mohm = 10.0


allowed_current_per_pin = derated_current_per_pin(
    rated_current_per_pin_a=rated_current_per_pin_a,
    derating_factor=derating_factor,
)

required_pins = pins_needed_for_current(
    total_current_a=total_current_a,
    rated_current_per_pin_a=rated_current_per_pin_a,
    derating_factor=derating_factor,
)

actual_current_per_pin = current_per_pin(
    total_current_a=total_current_a,
    number_of_pins=required_pins,
)

voltage_drop = connector_voltage_drop(
    total_current_a=total_current_a,
    contact_resistance_mohm=contact_resistance_mohm,
    number_of_parallel_pins=required_pins,
)

power_loss = connector_power_loss(
    total_current_a=total_current_a,
    contact_resistance_mohm=contact_resistance_mohm,
    number_of_parallel_pins=required_pins,
)

within_rating = is_current_within_connector_rating(
    total_current_a=total_current_a,
    number_of_pins=required_pins,
    rated_current_per_pin_a=rated_current_per_pin_a,
    derating_factor=derating_factor,
)


print("Connector Power Example")
print("-----------------------")
print(f"Rail voltage: {rail_voltage_v:.2f} V")
print(f"Total current: {total_current_a:.2f} A")
print(f"Rated current per pin: {rated_current_per_pin_a:.2f} A")
print(f"Derating factor: {derating_factor:.2f}")
print(f"Allowed current per pin: {allowed_current_per_pin:.2f} A")
print()
print(f"Required parallel pins: {required_pins}")
print(f"Actual current per pin: {actual_current_per_pin:.2f} A")
print(f"Within derated rating: {within_rating}")
print()
print(f"Contact resistance: {contact_resistance_mohm:.2f} mohm")
print(f"Connector voltage drop: {voltage_drop:.6f} V")
print(f"Connector power loss: {power_loss:.6f} W")
