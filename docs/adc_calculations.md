# ADC Calculations

ADC calculations are useful during schematic design, sensor scaling, embedded firmware bring-up, and hardware debugging.

This module helps answer questions such as:

- What is the LSB size of this ADC?
- What voltage does this ADC code represent?
- What ADC code should I expect for a measured voltage?
- How do I scale a 0-10 V sensor into a 3.3 V ADC input?

## ADC Max Code

For an ideal `N`-bit ADC, the maximum output code is:

```text
2^N - 1
```

For a 12-bit ADC:

```text
2^12 - 1 = 4095
```

Python example:

```python
from ee_pcb_toolkit.adc import adc_max_code

max_code = adc_max_code(resolution_bits=12)
print(max_code)
```

Output:

```text
4095
```

## ADC LSB Size

The LSB size is the voltage represented by one ADC count.

For an ideal unipolar ADC:

```text
LSB = Vref / 2^N
```

Python example:

```python
from ee_pcb_toolkit.adc import adc_lsb_size

lsb = adc_lsb_size(
    v_ref=3.3,
    resolution_bits=12,
)

print(lsb)
```

For a 3.3 V, 12-bit ADC, this is about:

```text
0.0008057 V/count
```

or:

```text
0.8057 mV/count
```

## ADC Voltage From Code

Use this during bring-up when firmware prints an ADC code and you want to estimate the measured voltage.

```python
from ee_pcb_toolkit.adc import adc_voltage_from_code

voltage = adc_voltage_from_code(
    code=2048,
    v_ref=3.3,
    resolution_bits=12,
)

print(voltage)
```

Approximate result:

```text
1.65 V
```

## ADC Code From Voltage

Use this when you know the expected voltage and want to predict the ADC reading.

```python
from ee_pcb_toolkit.adc import adc_code_from_voltage

code = adc_code_from_voltage(
    voltage_v=1.65,
    v_ref=3.3,
    resolution_bits=12,
)

print(code)
```

Approximate result:

```text
2048
```

## 0-10 V Sensor Scaling

A common hardware design problem is reading a 0-10 V sensor with a 3.3 V ADC.

The required divider ratio is:

```text
3.3 / 10 = 0.33
```

If `Rbottom = 10k`, the toolkit can calculate the required top resistor:

```python
from ee_pcb_toolkit.adc import adc_divider_r_top

r_top = adc_divider_r_top(
    vin_max=10.0,
    adc_vmax=3.3,
    r_bottom=10000,
)

print(r_top)
```

Approximate result:

```text
20303 ohms
```

A practical design would then choose a nearby standard resistor value and verify the final ADC voltage.

## Engineering Notes

These calculations are ideal estimates. Real ADC systems also depend on:

- ADC input impedance
- sample-and-hold capacitor behavior
- source impedance
- reference voltage tolerance
- resistor tolerance
- noise
- anti-aliasing filters
- PCB layout
- grounding and shielding

Use these calculations as first-pass design and bring-up tools, then verify with datasheets and measurements.
