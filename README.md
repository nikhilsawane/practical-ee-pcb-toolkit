# Practical EE & PCB Toolkit

A practical Python toolkit for electrical engineering, PCB layout, analog front-end design, power budgeting, and hardware bring-up calculations.

This project turns common engineering checks into small, reusable, tested Python tools. It can be used as an interactive command-line calculator or as a Python package inside your own scripts.

---

## Quick Start

Run the interactive calculator from the project root:

```bash
python -m ee_pcb_toolkit
```

Menu:

```text
Practical EE & PCB Toolkit
--------------------------
1. Voltage divider
2. RC cutoff frequency
3. PCB trace voltage drop
4. LDO power dissipation
5. Via planning for power net
6. ADC calculations
7. Op-amp calculations
8. Filter calculations
9. Connector calculations
10. Signal integrity calculations
11. PCB rule assistant
0. Exit
```

The `-m` flag tells Python to run the `ee_pcb_toolkit` package as a module. Python executes `ee_pcb_toolkit/__main__.py`, which launches the CLI in `ee_pcb_toolkit/cli.py`.

---

## Engineering-Friendly Input

The CLI accepts practical EE and PCB units directly:

```text
22 mil
0.45 mm
4.7k
10k
100 nF
10 uF
500 mA
2 A
1 ns
1 kHz
1 MHz
```

This avoids manual unit conversion while doing quick design checks.

---

## Current Tools

### PCB and Layout

- PCB trace resistance, voltage drop, and power loss
- Via resistance, voltage drop, power loss, and via-count planning
- Connector current derating, pin-count planning, voltage drop, and contact loss
- Signal integrity estimates: propagation delay, trace delay, edge bandwidth, wavelength, and lumped-length limit
- PCB rule assistant using LAIR/RADICALS-style Altium rules

### Analog and Mixed-Signal

- Voltage divider calculations
- RC cutoff frequency
- First-order low-pass and high-pass filter response
- ADC LSB size, code-to-voltage, voltage-to-code, and sensor divider planning
- Op-amp gain, output voltage, target feedback resistor, closed-loop bandwidth, and slew-rate checks

### Power and Thermal

- LDO power dissipation
- Buck regulator feedback resistor helper
- Efficiency and current-from-power helpers
- Junction temperature and max-power estimates

### Unit Helpers

- mil/mm/in conversions
- copper weight/thickness conversions
- parsing helpers for resistance, capacitance, voltage, current, frequency, length, time, plating, and copper weight

---

## PCB Rule Assistant

The PCB rule assistant includes project rules based on LAIR/RADICALS Altium-style constraints:

```text
Width_default:       min 8 mil,  preferred 8 mil,  max 12 mil
Width_Power:         min 8 mil,  preferred 12 mil, max 16 mil
Width_high_current:  min 8 mil,  preferred 30 mil, max 50 mil
Width_NTC_Net:       min 12 mil, preferred 12 mil, max 12 mil
Width_Heater_Net:    min 20 mil, preferred 20 mil, max 20 mil
```

Via rules:

```text
Default via: 24 mil pad / 12 mil drill
Power via:   26 mil pad / 12 mil drill
Legacy default via: 26 mil pad / 12 mil drill
Legacy power via:   30 mil pad / 15 mil drill
```

Differential-pair rules:

```text
100 ohm legacy: 7 mil width / 6 mil gap
100 ohm:        6 mil width / 10 mil gap
120 ohm:        5 mil width / 15 mil gap
```

Clearance starter rules:

```text
Default/digital: 6 mil
Plane:           12 mil
Board outline:   10 mil
Switching:       max(18 mil, 3x trace width)
```

Important design note: current primarily drives trace width. Voltage primarily drives clearance.

---

## Project Structure

```text
practical-ee-pcb-toolkit/
├── ee_pcb_toolkit/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── input_helpers.py
│   ├── units.py
│   ├── resistors.py
│   ├── capacitors.py
│   ├── pcb_traces.py
│   ├── power.py
│   ├── thermal.py
│   ├── vias.py
│   ├── adc.py
│   ├── opamps.py
│   ├── filters.py
│   ├── connectors.py
│   ├── signal_integrity.py
│   └── pcb_rules.py
├── examples/
│   ├── basic_usage.py
│   ├── via_power_net_example.py
│   ├── adc_bringup_example.py
│   ├── opamp_front_end_example.py
│   ├── filter_design_example.py
│   ├── connector_power_example.py
│   ├── signal_integrity_example.py
│   └── pcb_rules_example.py
├── docs/
├── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/nikhilsawane/practical-ee-pcb-toolkit.git
cd practical-ee-pcb-toolkit
python -m pip install -e .
python -m pip install -r requirements.txt
```

Run the CLI:

```bash
python -m ee_pcb_toolkit
```

---

## Running Examples

```bash
python examples/basic_usage.py
python examples/via_power_net_example.py
python examples/adc_bringup_example.py
python examples/opamp_front_end_example.py
python examples/filter_design_example.py
python examples/connector_power_example.py
python examples/signal_integrity_example.py
python examples/pcb_rules_example.py
```

---

## Python Usage Examples

### ADC Sensor Scaling

```python
from ee_pcb_toolkit.adc import adc_divider_r_top, sensor_voltage_to_adc_code

r_top = adc_divider_r_top(
    vin_max=10.0,
    adc_vmax=3.3,
    r_bottom=10000,
)

code = sensor_voltage_to_adc_code(
    sensor_voltage_v=5.0,
    r_top=r_top,
    r_bottom=10000,
    v_ref=3.3,
    resolution_bits=12,
)

print(r_top)
print(code)
```

### PCB Rule Assistant

```python
from ee_pcb_toolkit.pcb_rules import recommend_trace_width_mil

result = recommend_trace_width_mil(
    current_a=2.0,
    net_class="power_input",
    copper_oz=1.0,
    temperature_rise_c=10.0,
    layer="external",
)

print(result)
```

### Signal Integrity

```python
from ee_pcb_toolkit.signal_integrity import trace_delay_ns

print(trace_delay_ns(length_mm=100, relative_permittivity=4.0))
```

---

## Running Tests

```bash
python -m pytest -v
```

Current test coverage includes ADC, capacitors, connectors, filters, input parsing, op-amps, PCB traces, resistors, signal integrity, units, vias, and PCB rule helpers.

---

## Documentation

Docs are provided for the major calculation groups:

```text
docs/via_calculations.md
docs/adc_calculations.md
docs/opamp_calculations.md
docs/filter_calculations.md
docs/connector_calculations.md
```

---

## Engineering Notes

These tools are intended for quick engineering estimates, portfolio demonstration, and educational use.

For final PCB design decisions, verify against:

- component datasheets
- PCB manufacturer capabilities
- IPC guidance
- Altium project rules
- simulation
- lab measurements
- thermal and reliability requirements

The calculations are first-pass estimates. They do not replace formal design review, safety spacing requirements, or manufacturer signoff.

---

## Roadmap

Possible future additions:

- impedance helpers for microstrip and stripline geometry
- decoupling capacitor planning
- power-tree and rail-budget reports
- resistor/capacitor standard-value selection
- CSV BOM import and summary tools
- CLI export to Markdown or CSV

---

## License

MIT License
