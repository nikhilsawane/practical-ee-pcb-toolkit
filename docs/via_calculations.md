# Via Calculations

A via is a plated hole that connects one PCB layer to another.

In PCB design, vias are commonly used for:

- Moving signals between layers
- Connecting power rails to internal planes
- Connecting ground pours
- Thermal stitching
- Reducing impedance in power paths

For low-current signals, a single via is usually fine. For power nets, one via may not be enough.

## Why Via Calculations Matter

Every via has some resistance.

That resistance is small, but when current flows through the via, it creates:

- Voltage drop
- Power loss
- Local heating

The basic relationships are:

```text
V = I * R
P = I^2 * R
```

Where:

- `V` is voltage drop
- `I` is current
- `R` is resistance
- `P` is power loss

## Function: via_barrel_resistance()

```python
from ee_pcb_toolkit.vias import via_barrel_resistance

r_via = via_barrel_resistance(
    board_thickness_mm=1.6,
    finished_hole_diameter_mm=0.3,
    plating_thickness_um=25,
)
```

This estimates the resistance of one plated through via.

Use this when you want to know:

```text
How much resistance does this via add to my current path?
```

## Function: vias_needed()

```python
from ee_pcb_toolkit.vias import vias_needed

num_vias = vias_needed(
    total_current_a=2.0,
    current_per_via_a=0.5,
)
```

This calculates how many vias are needed for a current path.

In this example:

```text
2.0 A total current / 0.5 A per via = 4 vias
```

So the result is:

```text
4
```

This is useful when designing power nets in Altium.

## Function: via_array_equivalent_resistance()

```python
from ee_pcb_toolkit.vias import via_array_equivalent_resistance

r_array = via_array_equivalent_resistance(
    single_via_resistance_ohms=0.01,
    number_of_vias=4,
)
```

Multiple vias in parallel reduce the effective resistance.

If one via is `0.01 ohms`, then four identical vias in parallel are:

```text
0.01 / 4 = 0.0025 ohms
```

## Practical PCB Example

Suppose a 3.3 V rail carries 2 A and needs to move from the top layer to an internal power plane.

A conservative design assumption might be:

```text
0.5 A per via
```

Then:

```python
from ee_pcb_toolkit.vias import vias_needed

num_vias = vias_needed(
    total_current_a=2.0,
    current_per_via_a=0.5,
)

print(num_vias)
```

Output:

```text
4
```

PCB meaning:

```text
Use at least 4 vias for this power transition.
```

## Important Note

Via current capacity is not a universal fixed number.

It depends on:

- Finished hole size
- Plating thickness
- Board thickness
- Copper connection to planes
- Temperature rise limit
- Manufacturer capability
- Whether the via is isolated or connected to large copper areas

Because of that, this toolkit does not pretend that one via always carries a fixed amount of current.

Instead, the `vias_needed()` function makes you choose the allowed current per via based on your design rules, PCB manufacturer, or conservative engineering judgment.

## Engineering Use

Use these calculations during:

- Power net planning
- Layer transition checks
- PCB layout review
- Hardware bring-up preparation
- Design documentation
