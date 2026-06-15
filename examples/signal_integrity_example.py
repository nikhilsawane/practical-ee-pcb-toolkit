###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: signal_integrity_example.py
###################################################################################################################################

"""
Example: Signal integrity first-pass checks.

Scenario:
A fast digital signal is routed on an FR-4 PCB.

We want to estimate:
1. Propagation delay
2. Trace delay
3. Bandwidth from rise time
4. Whether the trace length should be treated as a transmission line
"""

from ee_pcb_toolkit.signal_integrity import (
    propagation_delay_ns_per_mm,
    trace_delay_ns,
    edge_rate_bandwidth_hz,
    lumped_length_limit_mm,
)


relative_permittivity = 4.0
trace_length_mm = 100
rise_time_s = 1e-9


delay_per_mm = propagation_delay_ns_per_mm(
    relative_permittivity=relative_permittivity,
)

total_delay = trace_delay_ns(
    length_mm=trace_length_mm,
    relative_permittivity=relative_permittivity,
)

bandwidth = edge_rate_bandwidth_hz(
    rise_time_s=rise_time_s,
)

lumped_limit = lumped_length_limit_mm(
    rise_time_s=rise_time_s,
    relative_permittivity=relative_permittivity,
)


print("Signal Integrity Example")
print("------------------------")
print(f"Relative permittivity: {relative_permittivity:.2f}")
print(f"Trace length: {trace_length_mm:.2f} mm")
print(f"Rise time: {rise_time_s:.3e} s")
print()
print(f"Propagation delay: {delay_per_mm:.6f} ns/mm")
print(f"Trace delay: {total_delay:.6f} ns")
print(f"Estimated edge bandwidth: {bandwidth:.2f} Hz")
print(f"Lumped-length limit: {lumped_limit:.2f} mm")
print()
print("If the trace is longer than the lumped-length limit,")
print("consider treating it as a transmission line.")
