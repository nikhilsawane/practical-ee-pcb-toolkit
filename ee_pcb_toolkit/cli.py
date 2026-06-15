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
from ee_pcb_toolkit.adc import (
    adc_lsb_size,
    adc_voltage_from_code,
    adc_code_from_voltage,
    adc_divider_r_top,
    adc_divider_output,
)
from ee_pcb_toolkit.opamps import (
    non_inverting_gain,
    inverting_gain,
    non_inverting_output,
    inverting_output,
    non_inverting_r_feedback_for_gain,
    inverting_r_feedback_for_gain,
    closed_loop_bandwidth,
    required_slew_rate_v_per_us,
)
from ee_pcb_toolkit.filters import (
    rc_cutoff_frequency as filter_rc_cutoff_frequency,
    rc_resistance_for_cutoff,
    rc_capacitance_for_cutoff,
    first_order_lowpass_gain,
    first_order_highpass_gain,
    lowpass_output_voltage,
    highpass_output_voltage,
    gain_to_db,
)
from ee_pcb_toolkit.connectors import (
    derated_current_per_pin,
    connector_total_current_capacity,
    pins_needed_for_current,
    current_per_pin,
    connector_voltage_drop,
    connector_power_loss,
    is_current_within_connector_rating,
)
from ee_pcb_toolkit.signal_integrity import (
    propagation_delay_ns_per_mm,
    trace_delay_ns,
    edge_rate_bandwidth_hz,
    wavelength_mm,
    quarter_wavelength_mm,
    lumped_length_limit_mm,
)
from ee_pcb_toolkit.pcb_rules import (
    recommend_trace_width_mil,
    voltage_clearance_recommendation_mil,
    via_rule_summary,
    get_diff_pair_rule,
)
from ee_pcb_toolkit.input_helpers import (
    get_engineering_value,
    LENGTH_TO_MM,
    RESISTANCE_TO_OHMS,
    CAPACITANCE_TO_FARADS,
    CURRENT_TO_AMPS,
    VOLTAGE_TO_VOLTS,
    PLATING_TO_UM,
    COPPER_WEIGHT_TO_OZ,
    FREQUENCY_TO_HZ,
    TIME_TO_SECONDS,
)


def get_int(prompt: str) -> int:
    """Get an integer from the user."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


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

    vin = get_engineering_value("Input voltage Vin [example: 5 V]: ", VOLTAGE_TO_VOLTS, "v")
    r_top = get_engineering_value("Top resistor R1 [example: 10k]: ", RESISTANCE_TO_OHMS, "ohm")
    r_bottom = get_engineering_value("Bottom resistor R2 [example: 4.7k]: ", RESISTANCE_TO_OHMS, "ohm")

    vout = voltage_divider(vin=vin, r_top=r_top, r_bottom=r_bottom)

    print(f"\nOutput voltage: {vout:.4f} V")


def rc_cutoff_calculator() -> None:
    print("\nRC Cutoff Frequency Calculator")
    print("------------------------------")

    resistance = get_engineering_value("Resistance [example: 10k]: ", RESISTANCE_TO_OHMS, "ohm")
    capacitance = get_engineering_value("Capacitance [example: 100 nF]: ", CAPACITANCE_TO_FARADS, "f")

    cutoff_frequency = rc_cutoff_frequency(
        r_ohms=resistance,
        c_farads=capacitance,
    )

    print(f"\nCutoff frequency: {cutoff_frequency:.4f} Hz")


def pcb_trace_calculator() -> None:
    print("\nPCB Trace Voltage Drop Calculator")
    print("---------------------------------")

    length_mm = get_engineering_value("Trace length [example: 70 mm]: ", LENGTH_TO_MM, "mm")
    width_mm = get_engineering_value("Trace width [example: 22 mil or 0.55 mm]: ", LENGTH_TO_MM, "mm")
    copper_oz = get_engineering_value("Copper weight [example: 1 oz or 2 oz]: ", COPPER_WEIGHT_TO_OZ, "oz")
    current_a = get_engineering_value("Current [example: 500 mA or 2 A]: ", CURRENT_TO_AMPS, "a")

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

    vin = get_engineering_value("Input voltage Vin [example: 5 V]: ", VOLTAGE_TO_VOLTS, "v")
    vout = get_engineering_value("Output voltage Vout [example: 3.3 V]: ", VOLTAGE_TO_VOLTS, "v")
    load_current = get_engineering_value("Load current [example: 500 mA]: ", CURRENT_TO_AMPS, "a")

    power = ldo_power_dissipation(
        vin=vin,
        vout=vout,
        load_current_a=load_current,
    )

    print(f"\nLDO power dissipation: {power:.4f} W")


def via_planning_calculator() -> None:
    print("\nVia Planning Calculator")
    print("-----------------------")

    total_current_a = get_engineering_value("Total current through power path [example: 2 A]: ", CURRENT_TO_AMPS, "a")
    allowed_current_per_via_a = get_engineering_value("Allowed current per via [example: 500 mA]: ", CURRENT_TO_AMPS, "a")
    board_thickness_mm = get_engineering_value("Board thickness [example: 1.6 mm]: ", LENGTH_TO_MM, "mm")
    finished_hole_diameter_mm = get_engineering_value("Finished via hole diameter [example: 0.3 mm or 12 mil]: ", LENGTH_TO_MM, "mm")
    plating_thickness_um = get_engineering_value("Via plating thickness [example: 25 um]: ", PLATING_TO_UM, "um")

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


def adc_calculator() -> None:
    print("\nADC Calculator")
    print("--------------")
    print("1. ADC voltage from code")
    print("2. ADC code from voltage")
    print("3. ADC divider for sensor input")
    print("0. Back to main menu")

    choice = input("\nSelect an ADC calculator: ").strip()

    if choice == "1":
        v_ref = get_engineering_value("ADC reference voltage [example: 3.3 V]: ", VOLTAGE_TO_VOLTS, "v")
        resolution_bits = get_int("ADC resolution [bits, example: 12]: ")
        code = get_int("ADC code [example: 2048]: ")

        voltage = adc_voltage_from_code(code=code, v_ref=v_ref, resolution_bits=resolution_bits)
        lsb = adc_lsb_size(v_ref=v_ref, resolution_bits=resolution_bits)

        print(f"\nADC LSB size: {lsb:.6f} V/count")
        print(f"ADC input voltage estimate: {voltage:.6f} V")

    elif choice == "2":
        voltage = get_engineering_value("ADC input voltage [example: 1.65 V]: ", VOLTAGE_TO_VOLTS, "v")
        v_ref = get_engineering_value("ADC reference voltage [example: 3.3 V]: ", VOLTAGE_TO_VOLTS, "v")
        resolution_bits = get_int("ADC resolution [bits, example: 12]: ")

        code = adc_code_from_voltage(voltage_v=voltage, v_ref=v_ref, resolution_bits=resolution_bits)
        lsb = adc_lsb_size(v_ref=v_ref, resolution_bits=resolution_bits)

        print(f"\nADC LSB size: {lsb:.6f} V/count")
        print(f"Expected ADC code: {code}")

    elif choice == "3":
        vin_max = get_engineering_value("Maximum sensor/input voltage [example: 10 V]: ", VOLTAGE_TO_VOLTS, "v")
        adc_vmax = get_engineering_value("Maximum ADC input voltage [example: 3.3 V]: ", VOLTAGE_TO_VOLTS, "v")
        r_bottom = get_engineering_value("Bottom resistor [example: 10k]: ", RESISTANCE_TO_OHMS, "ohm")

        r_top = adc_divider_r_top(vin_max=vin_max, adc_vmax=adc_vmax, r_bottom=r_bottom)
        actual_adc_vmax = adc_divider_output(vin=vin_max, r_top=r_top, r_bottom=r_bottom)

        print(f"\nTop resistor: {r_top:.2f} ohms")
        print(f"Bottom resistor: {r_bottom:.2f} ohms")
        print(f"ADC voltage at maximum input: {actual_adc_vmax:.4f} V")

    elif choice == "0":
        return

    else:
        print("Invalid ADC calculator selection.")


def opamp_calculator() -> None:
    print("\nOp-Amp Calculator")
    print("-----------------")
    print("1. Non-inverting amplifier output")
    print("2. Inverting amplifier output")
    print("3. Feedback resistor for target gain")
    print("4. Closed-loop bandwidth estimate")
    print("5. Required slew rate")
    print("0. Back to main menu")

    choice = input("\nSelect an op-amp calculator: ").strip()

    if choice == "1":
        vin = get_engineering_value("Input voltage [example: 0.5 V]: ", VOLTAGE_TO_VOLTS, "v")
        r_feedback = get_engineering_value("Feedback resistor Rf [example: 56k]: ", RESISTANCE_TO_OHMS, "ohm")
        r_ground = get_engineering_value("Ground resistor Rg [example: 10k]: ", RESISTANCE_TO_OHMS, "ohm")

        gain = non_inverting_gain(r_feedback=r_feedback, r_ground=r_ground)
        vout = non_inverting_output(vin=vin, r_feedback=r_feedback, r_ground=r_ground)

        print(f"\nNon-inverting gain: {gain:.4f}")
        print(f"Output voltage: {vout:.4f} V")

    elif choice == "2":
        vin = get_engineering_value("Input voltage [example: 0.5 V]: ", VOLTAGE_TO_VOLTS, "v")
        r_feedback = get_engineering_value("Feedback resistor Rf [example: 20k]: ", RESISTANCE_TO_OHMS, "ohm")
        r_input = get_engineering_value("Input resistor Rin [example: 10k]: ", RESISTANCE_TO_OHMS, "ohm")

        gain = inverting_gain(r_feedback=r_feedback, r_input=r_input)
        vout = inverting_output(vin=vin, r_feedback=r_feedback, r_input=r_input)

        print(f"\nInverting gain magnitude: {gain:.4f}")
        print(f"Output voltage: {vout:.4f} V")

    elif choice == "3":
        print("\n1. Non-inverting amplifier")
        print("2. Inverting amplifier")
        amp_type = input("Select amplifier type: ").strip()

        target_gain = get_float("Target gain [example: 3]: ")

        if amp_type == "1":
            r_ground = get_engineering_value("Ground resistor Rg [example: 10k]: ", RESISTANCE_TO_OHMS, "ohm")
            r_feedback = non_inverting_r_feedback_for_gain(target_gain=target_gain, r_ground=r_ground)
            print(f"\nRequired feedback resistor Rf: {r_feedback:.2f} ohms")

        elif amp_type == "2":
            r_input = get_engineering_value("Input resistor Rin [example: 10k]: ", RESISTANCE_TO_OHMS, "ohm")
            r_feedback = inverting_r_feedback_for_gain(target_gain=target_gain, r_input=r_input)
            print(f"\nRequired feedback resistor Rf: {r_feedback:.2f} ohms")

        else:
            print("Invalid amplifier type.")

    elif choice == "4":
        gbw = get_engineering_value("Op-amp gain-bandwidth product [example: 1 MHz]: ", FREQUENCY_TO_HZ, "hz")
        gain = get_float("Closed-loop gain [example: 10]: ")

        bandwidth = closed_loop_bandwidth(gain_bandwidth_hz=gbw, closed_loop_gain=gain)

        print(f"\nEstimated closed-loop bandwidth: {bandwidth:.2f} Hz")

    elif choice == "5":
        v_peak = get_engineering_value("Output peak voltage [example: 1 V]: ", VOLTAGE_TO_VOLTS, "v")
        frequency = get_engineering_value("Signal frequency [example: 100 kHz]: ", FREQUENCY_TO_HZ, "hz")

        slew_rate = required_slew_rate_v_per_us(v_peak=v_peak, frequency_hz=frequency)

        print(f"\nRequired slew rate: {slew_rate:.6f} V/us")

    elif choice == "0":
        return

    else:
        print("Invalid op-amp calculator selection.")


def filter_calculator() -> None:
    print("\nFilter Calculator")
    print("-----------------")
    print("1. RC cutoff from R and C")
    print("2. R or C for target cutoff")
    print("3. Low-pass response at frequency")
    print("4. High-pass response at frequency")
    print("0. Back to main menu")

    choice = input("\nSelect a filter calculator: ").strip()

    if choice == "1":
        resistance = get_engineering_value("Resistance [example: 10k]: ", RESISTANCE_TO_OHMS, "ohm")
        capacitance = get_engineering_value("Capacitance [example: 100 nF]: ", CAPACITANCE_TO_FARADS, "f")

        cutoff = filter_rc_cutoff_frequency(
            r_ohms=resistance,
            c_farads=capacitance,
        )

        print(f"\nCutoff frequency: {cutoff:.4f} Hz")

    elif choice == "2":
        print("\n1. Calculate resistor from cutoff and capacitor")
        print("2. Calculate capacitor from cutoff and resistor")
        solve_choice = input("Select what to calculate: ").strip()

        cutoff = get_engineering_value("Target cutoff frequency [example: 1 kHz]: ", FREQUENCY_TO_HZ, "hz")

        if solve_choice == "1":
            capacitance = get_engineering_value("Capacitance [example: 100 nF]: ", CAPACITANCE_TO_FARADS, "f")
            resistance = rc_resistance_for_cutoff(
                cutoff_hz=cutoff,
                c_farads=capacitance,
            )
            print(f"\nRequired resistor: {resistance:.2f} ohms")

        elif solve_choice == "2":
            resistance = get_engineering_value("Resistance [example: 10k]: ", RESISTANCE_TO_OHMS, "ohm")
            capacitance = rc_capacitance_for_cutoff(
                cutoff_hz=cutoff,
                r_ohms=resistance,
            )
            print(f"\nRequired capacitor: {capacitance:.12f} F")
            print(f"Required capacitor: {capacitance * 1e9:.4f} nF")

        else:
            print("Invalid selection.")

    elif choice == "3":
        vin = get_engineering_value("Input voltage magnitude [example: 1 V]: ", VOLTAGE_TO_VOLTS, "v")
        frequency = get_engineering_value("Signal frequency [example: 5 kHz]: ", FREQUENCY_TO_HZ, "hz")
        cutoff = get_engineering_value("Cutoff frequency [example: 1 kHz]: ", FREQUENCY_TO_HZ, "hz")

        gain = first_order_lowpass_gain(frequency_hz=frequency, cutoff_hz=cutoff)
        vout = lowpass_output_voltage(vin=vin, frequency_hz=frequency, cutoff_hz=cutoff)
        gain_db = gain_to_db(gain)

        print(f"\nLow-pass gain: {gain:.6f}")
        print(f"Low-pass gain: {gain_db:.2f} dB")
        print(f"Output voltage magnitude: {vout:.6f} V")

    elif choice == "4":
        vin = get_engineering_value("Input voltage magnitude [example: 1 V]: ", VOLTAGE_TO_VOLTS, "v")
        frequency = get_engineering_value("Signal frequency [example: 100 Hz]: ", FREQUENCY_TO_HZ, "hz")
        cutoff = get_engineering_value("Cutoff frequency [example: 1 kHz]: ", FREQUENCY_TO_HZ, "hz")

        gain = first_order_highpass_gain(frequency_hz=frequency, cutoff_hz=cutoff)
        vout = highpass_output_voltage(vin=vin, frequency_hz=frequency, cutoff_hz=cutoff)
        gain_db = gain_to_db(gain)

        print(f"\nHigh-pass gain: {gain:.6f}")
        print(f"High-pass gain: {gain_db:.2f} dB")
        print(f"Output voltage magnitude: {vout:.6f} V")

    elif choice == "0":
        return

    else:
        print("Invalid filter calculator selection.")



def connector_calculator() -> None:
    print("\nConnector Calculator")
    print("--------------------")
    print("1. Pins needed for current")
    print("2. Connector voltage drop and power loss")
    print("3. Check current against derated rating")
    print("0. Back to main menu")

    choice = input("\nSelect a connector calculator: ").strip()

    if choice == "1":
        total_current = get_engineering_value("Total current [example: 6 A]: ", CURRENT_TO_AMPS, "a")
        rated_current_per_pin = get_engineering_value("Rated current per pin [example: 2 A]: ", CURRENT_TO_AMPS, "a")
        derating_factor = get_float("Derating factor [example: 0.8]: ")

        allowed_current = derated_current_per_pin(
            rated_current_per_pin_a=rated_current_per_pin,
            derating_factor=derating_factor,
        )

        required_pins = pins_needed_for_current(
            total_current_a=total_current,
            rated_current_per_pin_a=rated_current_per_pin,
            derating_factor=derating_factor,
        )

        per_pin_current = current_per_pin(
            total_current_a=total_current,
            number_of_pins=required_pins,
        )

        total_capacity = connector_total_current_capacity(
            number_of_pins=required_pins,
            rated_current_per_pin_a=rated_current_per_pin,
            derating_factor=derating_factor,
        )

        print(f"\nAllowed current per pin: {allowed_current:.4f} A")
        print(f"Required parallel pins: {required_pins}")
        print(f"Current per pin with {required_pins} pins: {per_pin_current:.4f} A")
        print(f"Total derated capacity: {total_capacity:.4f} A")

    elif choice == "2":
        total_current = get_engineering_value("Total current [example: 6 A]: ", CURRENT_TO_AMPS, "a")
        contact_resistance = get_float("Contact resistance per pin [mohm, example: 10]: ")
        number_of_pins = get_int("Number of parallel pins [example: 4]: ")

        voltage_drop = connector_voltage_drop(
            total_current_a=total_current,
            contact_resistance_mohm=contact_resistance,
            number_of_parallel_pins=number_of_pins,
        )

        power_loss = connector_power_loss(
            total_current_a=total_current,
            contact_resistance_mohm=contact_resistance,
            number_of_parallel_pins=number_of_pins,
        )

        print(f"\nConnector voltage drop: {voltage_drop:.6f} V")
        print(f"Connector power loss: {power_loss:.6f} W")

    elif choice == "3":
        total_current = get_engineering_value("Total current [example: 6 A]: ", CURRENT_TO_AMPS, "a")
        number_of_pins = get_int("Number of parallel pins [example: 4]: ")
        rated_current_per_pin = get_engineering_value("Rated current per pin [example: 2 A]: ", CURRENT_TO_AMPS, "a")
        derating_factor = get_float("Derating factor [example: 0.8]: ")

        total_capacity = connector_total_current_capacity(
            number_of_pins=number_of_pins,
            rated_current_per_pin_a=rated_current_per_pin,
            derating_factor=derating_factor,
        )

        per_pin_current = current_per_pin(
            total_current_a=total_current,
            number_of_pins=number_of_pins,
        )

        within_rating = is_current_within_connector_rating(
            total_current_a=total_current,
            number_of_pins=number_of_pins,
            rated_current_per_pin_a=rated_current_per_pin,
            derating_factor=derating_factor,
        )

        print(f"\nCurrent per pin: {per_pin_current:.4f} A")
        print(f"Total derated capacity: {total_capacity:.4f} A")
        print(f"Within derated rating: {within_rating}")

    elif choice == "0":
        return

    else:
        print("Invalid connector calculator selection.")

def signal_integrity_calculator() -> None:
    print("\nSignal Integrity Calculator")
    print("---------------------------")
    print("1. Trace delay")
    print("2. Edge-rate bandwidth")
    print("3. Wavelength and quarter wavelength")
    print("4. Lumped-length limit")
    print("0. Back to main menu")

    choice = input("\nSelect a signal integrity calculator: ").strip()

    if choice == "1":
        length_mm = get_engineering_value("Trace length [example: 100 mm]: ", LENGTH_TO_MM, "mm")
        er = get_float("Relative permittivity / Er [example: 4.0]: ")

        delay_per_mm = propagation_delay_ns_per_mm(relative_permittivity=er)
        delay = trace_delay_ns(length_mm=length_mm, relative_permittivity=er)

        print(f"\nPropagation delay: {delay_per_mm:.6f} ns/mm")
        print(f"Trace delay: {delay:.6f} ns")

    elif choice == "2":
        rise_time = get_engineering_value("Rise time [example: 1 ns]: ", TIME_TO_SECONDS, "s")

        bandwidth = edge_rate_bandwidth_hz(rise_time_s=rise_time)

        print(f"\nEstimated edge bandwidth: {bandwidth:.2f} Hz")
        print(f"Estimated edge bandwidth: {bandwidth / 1e6:.2f} MHz")

    elif choice == "3":
        frequency = get_engineering_value("Frequency [example: 1 GHz]: ", FREQUENCY_TO_HZ, "hz")
        er = get_float("Relative permittivity / Er [example: 4.0]: ")

        wavelength = wavelength_mm(frequency_hz=frequency, relative_permittivity=er)
        quarter = quarter_wavelength_mm(frequency_hz=frequency, relative_permittivity=er)

        print(f"\nWavelength: {wavelength:.4f} mm")
        print(f"Quarter wavelength: {quarter:.4f} mm")

    elif choice == "4":
        rise_time = get_engineering_value("Rise time [example: 1 ns]: ", TIME_TO_SECONDS, "s")
        er = get_float("Relative permittivity / Er [example: 4.0]: ")
        fraction = get_float("Delay fraction of rise time [example: 0.1]: ")

        limit = lumped_length_limit_mm(
            rise_time_s=rise_time,
            relative_permittivity=er,
            fraction=fraction,
        )

        print(f"\nLumped-length limit: {limit:.4f} mm")
        print("If your trace is longer than this, consider transmission-line behavior.")

    elif choice == "0":
        return

    else:
        print("Invalid signal integrity calculator selection.")


def pcb_rules_calculator() -> None:
    print("\nPCB Rule Assistant")
    print("------------------")
    print("1. Recommend trace width from current and net class")
    print("2. Recommend starter clearance from voltage")
    print("3. Show via rule summary")
    print("4. Show differential-pair rule")
    print("0. Back to main menu")

    choice = input("\nSelect a PCB rule calculator: ").strip()

    if choice == "1":
        print("\nNet class options:")
        print("default, power, power_input, ntc, heater")

        net_class = input("Net class [example: power_input]: ").strip()
        current = get_engineering_value("Current [example: 2 A]: ", CURRENT_TO_AMPS, "a")
        copper_oz = get_engineering_value("Copper weight [example: 1 oz or 2 oz]: ", COPPER_WEIGHT_TO_OZ, "oz")
        temp_rise = get_float("Allowed temperature rise C [example: 10]: ")
        layer = input("Layer type [external/internal]: ").strip()

        recommendation = recommend_trace_width_mil(
            current_a=current,
            net_class=net_class,
            copper_oz=copper_oz,
            temperature_rise_c=temp_rise,
            layer=layer,
        )

        print("\nTrace-width recommendation:")
        print(f"Rule: {recommendation['rule_name']}")
        print(f"Required by current: {recommendation['required_by_current_mil']:.4f} mil")
        print(f"Rule min: {recommendation['rule_min_mil']:.4f} mil")
        print(f"Rule preferred: {recommendation['rule_preferred_mil']:.4f} mil")
        print(f"Rule max: {recommendation['rule_max_mil']:.4f} mil")
        print(f"Recommended min: {recommendation['recommended_min_mil']:.4f} mil")
        print(f"Recommended preferred: {recommendation['recommended_preferred_mil']:.4f} mil")
        print(f"Status: {recommendation['status']}")

    elif choice == "2":
        print("\nClearance type options:")
        print("default, digital, plane, board_outline, switching")

        voltage = get_engineering_value("Voltage [example: 24 V]: ", VOLTAGE_TO_VOLTS, "v")
        clearance_type = input("Clearance type [example: default]: ").strip()

        trace_width_mil = None

        if clearance_type.strip().lower() == "switching":
            trace_width_mil = get_float("Trace width in mil [example: 6]: ")

        result = voltage_clearance_recommendation_mil(
            voltage_v=voltage,
            clearance_type=clearance_type,
            trace_width_mil=trace_width_mil,
        )

        print(f"\nRecommended clearance: {result['recommended_clearance_mil']:.4f} mil")
        print(result["note"])

    elif choice == "3":
        print("\nVia rule options:")
        print("default, power, legacy_default, legacy_power")

        rule_name = input("Via rule [example: default]: ").strip()
        summary = via_rule_summary(rule_name)

        print("\nVia rule summary:")
        print(f"Rule: {summary['rule_name']}")
        print(f"Pad diameter: {summary['pad_diameter_mil']:.4f} mil")
        print(f"Drill diameter: {summary['drill_diameter_mil']:.4f} mil")
        print(f"Annular ring: {summary['annular_ring_mil']:.4f} mil")
        print(f"Meets annular ring rule: {summary['meets_annular_ring']}")

    elif choice == "4":
        print("\nDiff-pair rule options:")
        print("diff100_legacy, diff100, diff120")

        rule_name = input("Diff-pair rule [example: diff100_legacy]: ").strip()
        rule = get_diff_pair_rule(rule_name)

        print("\nDifferential-pair rule:")
        print(f"Rule: {rule['name']}")
        print(f"Target impedance: {rule['target_impedance_ohms']:.1f} ohms")
        print(f"Width: {rule['width_mil']:.4f} mil")
        print(f"Gap: {rule['gap_mil']:.4f} mil")
        print(rule["description"])

    elif choice == "0":
        return

    else:
        print("Invalid PCB rule calculator selection.")

def print_menu() -> None:
    print("\nPractical EE & PCB Toolkit")
    print("--------------------------")
    print("1. Voltage divider")
    print("2. RC cutoff frequency")
    print("3. PCB trace voltage drop")
    print("4. LDO power dissipation")
    print("5. Via planning for power net")
    print("6. ADC calculations")
    print("7. Op-amp calculations")
    print("8. Filter calculations")
    print("9. Connector calculations")
    print("10. Signal integrity calculations")
    print("11. PCB rule assistant")
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
        elif choice == "6":
            adc_calculator()
        elif choice == "7":
            opamp_calculator()
        elif choice == "8":
            filter_calculator()
        elif choice == "9":
            connector_calculator()
        elif choice == "10":
            signal_integrity_calculator()
        elif choice == "11":
            pcb_rules_calculator()
        elif choice == "0":
            print("Exiting Practical EE & PCB Toolkit.")
            break
        else:
            print("Invalid selection. Please choose a valid menu option.")


if __name__ == "__main__":
    main()

