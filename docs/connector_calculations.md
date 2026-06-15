# Connector Calculations

Connector calculations are useful for power-entry design, board-to-board connectors, harness connectors, and current-sharing checks.

This module helps answer questions such as:

- How many connector pins do I need for this current?
- What is the derated current per pin?
- How much current flows through each parallel pin?
- How much voltage drop is caused by contact resistance?
- How much power is lost in the connector contacts?

## Derated Current Per Pin

Connector current ratings should often be derated. For example, a pin rated for `2 A` with an `80%` derating factor gives:

```text
2 A * 0.8 = 1.6 A
```

Python example:

```python
from ee_pcb_toolkit.connectors import derated_current_per_pin

allowed_current = derated_current_per_pin(
    rated_current_per_pin_a=2.0,
    derating_factor=0.8,
)

print(allowed_current)
```

## Pins Needed for Current

```python
from ee_pcb_toolkit.connectors import pins_needed_for_current

pins = pins_needed_for_current(
    total_current_a=6.0,
    rated_current_per_pin_a=2.0,
    derating_factor=0.8,
)

print(pins)
```

Result:

```text
4
```

## Current Per Pin

```python
from ee_pcb_toolkit.connectors import current_per_pin

current = current_per_pin(
    total_current_a=6.0,
    number_of_pins=4,
)

print(current)
```

Result:

```text
1.5 A
```

## Connector Voltage Drop

Contact resistance creates voltage drop. If each contact is `10 milliohms` and four contacts are used in parallel, the equivalent contact resistance is:

```text
10 milliohms / 4 = 2.5 milliohms
```

At `6 A`, the voltage drop is:

```text
6 A * 0.0025 ohms = 0.015 V
```

Python example:

```python
from ee_pcb_toolkit.connectors import connector_voltage_drop

v_drop = connector_voltage_drop(
    total_current_a=6.0,
    contact_resistance_mohm=10.0,
    number_of_parallel_pins=4,
)

print(v_drop)
```

## Connector Power Loss

```python
from ee_pcb_toolkit.connectors import connector_power_loss

power = connector_power_loss(
    total_current_a=6.0,
    contact_resistance_mohm=10.0,
    number_of_parallel_pins=4,
)

print(power)
```

Result:

```text
0.09 W
```

## Engineering Notes

These calculations are first-pass estimates. Real connector performance also depends on contact plating, mating cycles, temperature rise, wire gauge, PCB copper, airflow, enclosure temperature, vibration, contamination, and manufacturer rating conditions.

Use these calculations to plan pin count and estimate losses, then verify against the connector datasheet and system requirements.
