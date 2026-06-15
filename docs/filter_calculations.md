# Filter Calculations

Filter calculations are useful during analog front-end design, ADC input filtering, sensor conditioning, noise reduction, and hardware bring-up.

This module focuses on first-order RC low-pass and high-pass filters.

## RC Cutoff Frequency

For a first-order RC filter:

```text
fc = 1 / (2 * pi * R * C)
```

Example:

```python
from ee_pcb_toolkit.filters import rc_cutoff_frequency

fc = rc_cutoff_frequency(
    r_ohms=10000,
    c_farads=100e-9,
)

print(fc)
```

Approximate result:

```text
159.15 Hz
```

## Resistor for Target Cutoff

```python
from ee_pcb_toolkit.filters import rc_resistance_for_cutoff

r = rc_resistance_for_cutoff(
    cutoff_hz=1000,
    c_farads=100e-9,
)

print(r)
```

Approximate result:

```text
1591.55 ohms
```

## Capacitor for Target Cutoff

```python
from ee_pcb_toolkit.filters import rc_capacitance_for_cutoff

c = rc_capacitance_for_cutoff(
    cutoff_hz=1000,
    r_ohms=10000,
)

print(c)
```

Approximate result:

```text
15.9 nF
```

## Low-Pass Gain

At the cutoff frequency, a first-order low-pass filter has a gain of about `0.707`, which is about `-3 dB`.

```python
from ee_pcb_toolkit.filters import first_order_lowpass_gain, gain_to_db

gain = first_order_lowpass_gain(
    frequency_hz=1000,
    cutoff_hz=1000,
)

print(gain)
print(gain_to_db(gain))
```

## High-Pass Gain

At the cutoff frequency, a first-order high-pass filter also has a gain of about `0.707`, which is about `-3 dB`.

```python
from ee_pcb_toolkit.filters import first_order_highpass_gain

gain = first_order_highpass_gain(
    frequency_hz=1000,
    cutoff_hz=1000,
)

print(gain)
```

## Output Voltage Estimate

```python
from ee_pcb_toolkit.filters import lowpass_output_voltage

vout = lowpass_output_voltage(
    vin=1.0,
    frequency_hz=5000,
    cutoff_hz=1000,
)

print(vout)
```

Approximate result:

```text
0.196 V
```

## Engineering Notes

These calculations are ideal first-order estimates. Real filters also depend on component tolerance, source impedance, loading, parasitics, ADC sample-and-hold behavior, noise requirements, and PCB layout.

For ADC inputs, check the ADC datasheet for source impedance and sampling requirements.
