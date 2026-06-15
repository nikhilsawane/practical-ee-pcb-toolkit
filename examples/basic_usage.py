from ee_pcb_toolkit.resistors import voltage_divider
from ee_pcb_toolkit.capacitors import rc_cutoff_frequency
from ee_pcb_toolkit.pcb_traces import trace_resistance, trace_voltage_drop, trace_power_loss
from ee_pcb_toolkit.power import buck_feedback_r_top
from ee_pcb_toolkit.thermal import junction_temperature


vout = voltage_divider(vin=5.0, r_top=10000, r_bottom=10000)
print(f"Voltage divider output: {vout:.2f} V")

fc = rc_cutoff_frequency(r_ohms=10000, c_farads=100e-9)
print(f"RC cutoff frequency: {fc:.2f} Hz")

r_trace = trace_resistance(length_mm=100, width_mm=0.25, copper_oz=1.0)
v_drop = trace_voltage_drop(current_a=1.0, resistance_ohms=r_trace)
p_loss = trace_power_loss(current_a=1.0, resistance_ohms=r_trace)

print(f"Trace resistance: {r_trace:.4f} ohms")
print(f"Trace voltage drop: {v_drop:.4f} V")
print(f"Trace power loss: {p_loss:.4f} W")

r_top = buck_feedback_r_top(vout=3.3, v_ref=0.8, r_bottom=10000)
print(f"Buck top feedback resistor: {r_top:.1f} ohms")

tj = junction_temperature(ambient_c=25, power_w=0.8, theta_ja_c_per_w=45)
print(f"Estimated junction temperature: {tj:.1f} C")
