###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: pcb_rules_example.py
###################################################################################################################################

"""
Example: PCB rule assistant.

This example uses LAIR/RADICALS-style Altium rules and current-based width estimation.
"""

from ee_pcb_toolkit.pcb_rules import (
    recommend_trace_width_mil,
    voltage_clearance_recommendation_mil,
    via_rule_summary,
)


signal_recommendation = recommend_trace_width_mil(
    current_a=0.5,
    net_class="default",
    copper_oz=1.0,
    temperature_rise_c=10.0,
    layer="external",
)

power_recommendation = recommend_trace_width_mil(
    current_a=2.0,
    net_class="power_input",
    copper_oz=1.0,
    temperature_rise_c=10.0,
    layer="external",
)

default_clearance = voltage_clearance_recommendation_mil(
    voltage_v=24,
    clearance_type="default",
)

switching_clearance = voltage_clearance_recommendation_mil(
    voltage_v=24,
    clearance_type="switching",
    trace_width_mil=6,
)

default_via = via_rule_summary("default")
power_via = via_rule_summary("power")


print("PCB Rule Assistant Example")
print("--------------------------")
print()
print("Default signal trace:")
for key, value in signal_recommendation.items():
    print(f"  {key}: {value}")

print()
print("Power-input trace:")
for key, value in power_recommendation.items():
    print(f"  {key}: {value}")

print()
print("Clearance:")
print(f"  Default clearance: {default_clearance['recommended_clearance_mil']} mil")
print(f"  Switching clearance: {switching_clearance['recommended_clearance_mil']} mil")

print()
print("Via rules:")
print(f"  Default via: {default_via}")
print(f"  Power via: {power_via}")
