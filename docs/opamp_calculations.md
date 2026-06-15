# Op-Amp Calculations

Op-amp calculations are useful for analog front-end design, sensor signal conditioning, ADC input scaling, gain stages, and hardware bring-up.

This module helps answer questions such as:

- What gain do these resistors create?
- What output voltage should I expect?
- What feedback resistor do I need for a target gain?
- Is the op-amp gain-bandwidth product enough?
- What slew rate do I need for this signal?

## Non-Inverting Amplifier Gain

For a non-inverting amplifier:

```text
Gain = 1 + Rf / Rg
```

Python example:

```python
from ee_pcb_toolkit.opamps import non_inverting_gain

gain = non_inverting_gain(
    r_feedback=56000,
    r_ground=10000,
)

print(gain)
```

Result:

```text
6.6
```

## Non-Inverting Output Voltage

```python
from ee_pcb_toolkit.opamps import non_inverting_output

vout = non_inverting_output(
    vin=0.5,
    r_feedback=56000,
    r_ground=10000,
)

print(vout)
```

Result:

```text
3.3 V
```

This is a practical example of amplifying a 0.5 V sensor signal to nearly the full range of a 3.3 V ADC.

## Inverting Amplifier Gain

For an inverting amplifier, the gain magnitude is:

```text
Gain = Rf / Rin
```

The output is inverted, so the output voltage is negative for a positive input in an ideal dual-supply circuit.

```python
from ee_pcb_toolkit.opamps import inverting_output

vout = inverting_output(
    vin=0.5,
    r_feedback=20000,
    r_input=10000,
)

print(vout)
```

Result:

```text
-1.0 V
```

## Feedback Resistor for Target Gain

For a non-inverting amplifier:

```text
Rf = Rg * (Gain - 1)
```

```python
from ee_pcb_toolkit.opamps import non_inverting_r_feedback_for_gain

r_feedback = non_inverting_r_feedback_for_gain(
    target_gain=3.0,
    r_ground=10000,
)

print(r_feedback)
```

Result:

```text
20000 ohms
```

## Closed-Loop Bandwidth Estimate

A simple first-order estimate is:

```text
Closed-loop bandwidth = GBW / closed-loop gain
```

```python
from ee_pcb_toolkit.opamps import closed_loop_bandwidth

bandwidth = closed_loop_bandwidth(
    gain_bandwidth_hz=1_000_000,
    closed_loop_gain=10,
)

print(bandwidth)
```

Result:

```text
100000 Hz
```

## Required Slew Rate

For a sine wave:

```text
Slew rate = 2 * pi * frequency * Vpeak
```

```python
from ee_pcb_toolkit.opamps import required_slew_rate_v_per_us

slew_rate = required_slew_rate_v_per_us(
    v_peak=1.0,
    frequency_hz=100_000,
)

print(slew_rate)
```

Result:

```text
0.628 V/us
```

## Engineering Notes

These calculations are ideal estimates. Real op-amp design also depends on:

- input common-mode range
- output swing limits
- supply voltage
- load current
- stability and phase margin
- input bias current
- offset voltage
- noise
- gain-bandwidth product
- slew rate
- PCB layout and decoupling

Use these calculations as first-pass design and bring-up tools, then verify with datasheets, simulation, and measurements.
