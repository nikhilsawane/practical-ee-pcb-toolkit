import pytest

from ee_pcb_toolkit.adc import (
    adc_max_code,
    adc_lsb_size,
    adc_voltage_from_code,
    adc_code_from_voltage,
    adc_percent_full_scale,
    adc_divider_ratio,
    adc_divider_r_top,
    adc_divider_output,
    sensor_voltage_to_adc_code,
)


def test_adc_max_code_12_bit():
    assert adc_max_code(12) == 4095


def test_adc_lsb_size_12_bit():
    assert adc_lsb_size(v_ref=3.3, resolution_bits=12) == pytest.approx(3.3 / 4096)


def test_adc_voltage_from_code_midscale():
    assert adc_voltage_from_code(code=2048, v_ref=3.3, resolution_bits=12) == pytest.approx(1.65)


def test_adc_code_from_voltage_midscale():
    assert adc_code_from_voltage(voltage_v=1.65, v_ref=3.3, resolution_bits=12) == 2048


def test_adc_code_saturates_at_max():
    assert adc_code_from_voltage(voltage_v=3.3, v_ref=3.3, resolution_bits=12) == 4095


def test_adc_percent_full_scale():
    assert adc_percent_full_scale(code=4095, resolution_bits=12) == pytest.approx(100)


def test_adc_divider_ratio():
    assert adc_divider_ratio(vin_max=10.0, adc_vmax=3.3) == pytest.approx(0.33)


def test_adc_divider_r_top():
    r_top = adc_divider_r_top(
        vin_max=10.0,
        adc_vmax=3.3,
        r_bottom=10000,
    )

    assert r_top == pytest.approx(20303.0303, rel=1e-5)


def test_adc_divider_output():
    vout = adc_divider_output(
        vin=10.0,
        r_top=20303.0303,
        r_bottom=10000,
    )

    assert vout == pytest.approx(3.3, rel=1e-5)


def test_sensor_voltage_to_adc_code():
    code = sensor_voltage_to_adc_code(
        sensor_voltage_v=5.0,
        r_top=20303.0303,
        r_bottom=10000,
        v_ref=3.3,
        resolution_bits=12,
    )

    assert code == pytest.approx(2048, abs=1)
