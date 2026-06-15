# Practical EE & PCB Toolkit

A practical Python toolkit for electrical engineering and PCB design calculations.

This project collects common calculations used during schematic design, PCB layout, power budgeting, component sizing, and hardware bring-up. The goal is to turn repeated engineering calculations into small, reusable, tested Python functions.

## Project Goals

* Build a practical calculator library for EE and PCB design work
* Keep each function simple, readable, and reusable
* Provide examples that show real engineering use cases
* Add tests for each calculation module
* Document the assumptions behind each calculator

## Current Features

### Unit Conversions

* mils to millimeters
* millimeters to mils
* inches to millimeters
* millimeters to inches
* copper weight to copper thickness
* copper thickness to copper weight

### Resistor Calculations

* series resistance
* parallel resistance
* voltage divider output
* LED current-limiting resistor

### Capacitor and RC Calculations

* RC time constant
* RC cutoff frequency
* capacitor reactance

### PCB Trace Calculations

* trace cross-sectional area
* trace resistance
* trace voltage drop
* trace power loss

### Power Electronics Helpers

* LDO power dissipation
* buck regulator feedback resistor calculation
* efficiency calculation
* current from power and voltage

### Thermal Calculations

* estimated junction temperature
* maximum power for a junction temperature limit

### Via Calculations

* via barrel cross-sectional area
* via barrel resistance
* via voltage drop
* via power loss
* number of vias needed for a power net
* equivalent resistance of multiple vias in parallel

## Project Structure

```text
practical-ee-pcb-toolkit/
│
├── ee_pcb_toolkit/
│   ├── __init__.py
│   ├── units.py
│   ├── resistors.py
│   ├── capacitors.py
│   ├── pcb_traces.py
│   ├── power.py
│   ├── thermal.py
│   └── vias.py
│
├── examples/
│   ├── basic_usage.py
│   └── via_power_net_example.py
│
├── docs/
│   └── via_calculations.md
│
├── tests/
│   ├── test_units.py
│   ├── test_resistors.py
│   ├── test_capacitors.py
│   ├── test_pcb_traces.py
│   └── test_vias.py
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/nikhilsawane/practical-ee-pcb-toolkit.git
cd practical-ee-pcb-toolkit
```

Install the package in editable mode:

```bash
python -m pip install -e .
```

Install test dependencies:

```bash
python -m pip install -r requirements.txt
```

## Basic Usage

```python
from ee_pcb_toolkit.resistors import voltage_divider

vout = voltage_divider(
    vin=5.0,
    r_top=10000,
    r_bottom=10000,
)

print(vout)
```

Output:

```text
2.5
```

## Example: PCB Trace Resistance

```python
from ee_pcb_toolkit.pcb_traces import (
    trace_resistance,
    trace_voltage_drop,
    trace_power_loss,
)

r_trace = trace_resistance(
    length_mm=100,
    width_mm=0.25,
    copper_oz=1.0,
)

v_drop = trace_voltage_drop(
    current_a=1.0,
    resistance_ohms=r_trace,
)

p_loss = trace_power_loss(
    current_a=1.0,
    resistance_ohms=r_trace,
)

print(r_trace)
print(v_drop)
print(p_loss)
```

## Example: Via Planning for a Power Net

```python
from ee_pcb_toolkit.vias import (
    via_barrel_resistance,
    vias_needed,
    via_array_equivalent_resistance,
)

single_via_resistance = via_barrel_resistance(
    board_thickness_mm=1.6,
    finished_hole_diameter_mm=0.3,
    plating_thickness_um=25,
)

number_of_vias = vias_needed(
    total_current_a=2.0,
    current_per_via_a=0.5,
)

via_array_resistance = via_array_equivalent_resistance(
    single_via_resistance_ohms=single_via_resistance,
    number_of_vias=number_of_vias,
)

print(single_via_resistance)
print(number_of_vias)
print(via_array_resistance)
```

This example asks:

```text
If a 2 A power rail moves between PCB layers, and each via is conservatively limited to 0.5 A, how many vias should be used?
```

Result:

```text
4 vias
```

## Running Examples

Run the basic usage example:

```bash
python examples/basic_usage.py
```

Run the via power net example:

```bash
python examples/via_power_net_example.py
```

## Running Tests

```bash
python -m pytest -v
```

## Documentation

* [Via Calculations](docs/via_calculations.md)

## Engineering Notes

These tools are intended for quick engineering estimates and educational use.

For final PCB design decisions, values should be checked against:

* component datasheets
* PCB manufacturer capabilities
* IPC guidance
* simulation
* lab measurements
* thermal and reliability requirements

For example, via current capacity is not a universal fixed number. It depends on via size, plating thickness, board stackup, copper connection, temperature rise, and manufacturer process limits.

## Roadmap

Planned future modules:

* `adc.py` — ADC resolution, code-to-voltage, voltage-to-code, sensor scaling
* `opamps.py` — gain, offset, bandwidth, and basic amplifier calculations
* `filters.py` — low-pass, high-pass, and simple active filter helpers
* `transmission_lines.py` — impedance and signal integrity helper calculations
* `connectors.py` — pin current derating and connector power checks
* `bom.py` — basic component and power budget helpers

## License

MIT License
