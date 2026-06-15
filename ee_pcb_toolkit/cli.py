###################################################################################################################################
# Name: Nikhil Sawane
# Date: June 15, 2026
# Project: Practical EE & PCB Toolkit
# File: cli.py
###################################################################################################################################

"""
Command-line interface for the Practical EE & PCB Toolkit.

Run with:

python -m ee_pcb_toolkit
"""

from ee_pcb_toolkit.resistors import voltage_divider
from ee_pcb_toolkit.capacitors import rc_cutoff_frequency
from ee_pcb_toolkit.pcb_traces import trace_resistance, trace_voltage_drop, trace_power_loss
from ee_pcb_toolkit.power import ldo_power_dissipation
from ee_pcb_toolkit.vias import (
    via_barrel_resistance,
    vias_needed,
    via_array_equivalent_resistance,
    via_voltage_drop,
    via_power_loss,
)


def get_float(prompt: str) -> float:
    """Get a floating-point number from the user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def voltage_divider_calculator() -> None:
    print("\nVoltage Divider Calculator")
    print("--------------------------")

    vin = get_float("Input voltage Vin [V]: ")
    r_top = get_float("Top resistor R1 [ohms]: ")
    r_bottom = get_float("Bottom resistor R2 [ohms]: ")

    vout = voltage_divider(vin=vin, r_top=r_top, r_bottom=r_bottom)

    print(f"\nOutput voltage: {vout:.4f} V")


def rc_cutoff_calculator() -> None:
    print("\nRC Cutoff Frequency Calculator")
    print("------------------------------")

    resistance = get_float("Resistance [ohms]: ")
    capacitance = get_float("Capacitance [farads]: ")

    cutoff_frequency = rc_cutoff_frequency(
        r_ohms=resistance,
        c_farads=capacitance,
    )

    print(f"\nCutoff frequency: {cutoff_frequency:.4f} Hz")


def pcb_trace_calculator() -> None:
    print("\nPCB Trace Voltage Drop Calculator")
    print("---------------------------------")

    length_mm = get_float("Trace length [mm]: ")
    width_mm = get_float("Trace width [mm]: ")
    copper_oz = get_float("Copper weight [oz]: ")
    current_a = get_float("Current [A]: ")

    resistance = trace_resistance(
        length_mm=length_mm,
        width_mm=width_mm,
        copper_oz=copper_oz,
    )

    voltage_drop = trace_voltage_drop(
        current_a=current_a,
        resistance_ohms=resistance,
    )

    power_loss = trace_power_loss(
        current_a=current_a,
        resistance_ohms=resistance,
    )

    print(f"\nTrace resistance: {resistance:.6f} ohms")
    print(f"Voltage drop: {voltage_drop:.6f} V")
    print(f"Power loss: {power_loss:.6f} W")


def ldo_calculator() -> None:
    print("\nLDO Power Dissipation Calculator")
    print("--------------------------------")

    vin = get_float("Input voltage Vin [V]: ")
    vout = get_float("Output voltage Vout [V]: ")
    load_current = get_float("Load current [A]: ")

    power = ldo_power_dissipation(
        vin=vin,
        vout=vout,
        load_current_a=load_current,
    )

    print(f"\nLDO power dissipation: {power:.4f} W")


def via_planning_calculator() -> None:
    print("\nVia Planning Calculator")
    print("-----------------------")

    total_current_a = get_float("Total current through power path [A]: ")
    allowed_current_per_via_a = get_float("Allowed current per via [A]: ")
    board_thickness_mm = get_float("Board thickness [mm]: ")
    finished_hole_diameter_mm = get_float("Finished via hole diameter [mm]: ")
    plating_thickness_um = get_float("Via plating thickness [um]: ")

    single_via_resistance = via_barrel_resistance(
        board_thickness_mm=board_thickness_mm,
        finished_hole_diameter_mm=finished_hole_diameter_mm,
        plating_thickness_um=plating_thickness_um,
    )

    number_of_vias = vias_needed(
        total_current_a=total_current_a,
        current_per_via_a=allowed_current_per_via_a,
    )

    via_array_resistance = via_array_equivalent_resistance(
        single_via_resistance_ohms=single_via_resistance,
        number_of_vias=number_of_vias,
    )

    voltage_drop = via_voltage_drop(
        current_a=total_current_a,
        via_resistance_ohms=via_array_resistance,
    )

    power_loss = via_power_loss(
        current_a=total_current_a,
        via_resistance_ohms=via_array_resistance,
    )

    print(f"\nSingle via resistance: {single_via_resistance:.6f} ohms")
    print(f"Recommended number of vias: {number_of_vias}")
    print(f"Via array resistance: {via_array_resistance:.6f} ohms")
    print(f"Voltage drop through via array: {voltage_drop:.6f} V")
    print(f"Power loss in via array: {power_loss:.6f} W")


def print_menu() -> None:
    print("\nPractical EE & PCB Toolkit")
    print("--------------------------")
    print("1. Voltage divider")
    print("2. RC cutoff frequency")
    print("3. PCB trace voltage drop")
    print("4. LDO power dissipation")
    print("5. Via planning for power net")
    print("0. Exit")


def main() -> None:
    while True:
        print_menu()
        choice = input("\nSelect a calculator: ").strip()

        if choice == "1":
            voltage_divider_calculator()
        elif choice == "2":
            rc_cutoff_calculator()
        elif choice == "3":
            pcb_trace_calculator()
        elif choice == "4":
            ldo_calculator()
        elif choice == "5":
            via_planning_calculator()
        elif choice == "0":
            print("Exiting Practical EE & PCB Toolkit.")
            break
        else:
            print("Invalid selection. Please choose a valid menu option.")


if __name__ == "__main__":
    main()
