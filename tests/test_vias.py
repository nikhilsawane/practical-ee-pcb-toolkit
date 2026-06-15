import pytest

from ee_pcb_toolkit.vias import (
    via_barrel_cross_section_area_m2,
    via_barrel_resistance,
    via_voltage_drop,
    via_power_loss,
    vias_needed,
    via_array_equivalent_resistance,
)


def test_via_barrel_cross_section_area_positive():
    area = via_barrel_cross_section_area_m2(
        finished_hole_diameter_mm=0.3,
        plating_thickness_um=25,
    )

    assert area > 0


def test_via_barrel_resistance_positive():
    resistance = via_barrel_resistance(
        board_thickness_mm=1.6,
        finished_hole_diameter_mm=0.3,
        plating_thickness_um=25,
    )

    assert resistance > 0


def test_via_voltage_drop():
    assert via_voltage_drop(current_a=1.0, via_resistance_ohms=0.01) == pytest.approx(0.01)


def test_via_power_loss():
    assert via_power_loss(current_a=2.0, via_resistance_ohms=0.01) == pytest.approx(0.04)


def test_vias_needed():
    assert vias_needed(total_current_a=2.5, current_per_via_a=0.5) == 5


def test_via_array_equivalent_resistance():
    assert via_array_equivalent_resistance(
        single_via_resistance_ohms=0.01,
        number_of_vias=4,
    ) == pytest.approx(0.0025)
