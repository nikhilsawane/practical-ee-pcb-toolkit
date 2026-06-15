import pytest

from ee_pcb_toolkit.connectors import (
    derated_current_per_pin,
    connector_total_current_capacity,
    pins_needed_for_current,
    current_per_pin,
    contact_resistance_ohms,
    equivalent_parallel_contact_resistance,
    connector_voltage_drop,
    connector_power_loss,
    is_current_within_connector_rating,
)


def test_derated_current_per_pin():
    assert derated_current_per_pin(rated_current_per_pin_a=2.0, derating_factor=0.8) == pytest.approx(1.6)


def test_connector_total_current_capacity():
    assert connector_total_current_capacity(
        number_of_pins=4,
        rated_current_per_pin_a=2.0,
        derating_factor=0.8,
    ) == pytest.approx(6.4)


def test_pins_needed_for_current():
    assert pins_needed_for_current(
        total_current_a=6.0,
        rated_current_per_pin_a=2.0,
        derating_factor=0.8,
    ) == 4


def test_current_per_pin():
    assert current_per_pin(total_current_a=6.0, number_of_pins=4) == pytest.approx(1.5)


def test_contact_resistance_ohms():
    assert contact_resistance_ohms(contact_resistance_mohm=10) == pytest.approx(0.01)


def test_equivalent_parallel_contact_resistance():
    assert equivalent_parallel_contact_resistance(
        contact_resistance_mohm=10,
        number_of_parallel_pins=4,
    ) == pytest.approx(0.0025)


def test_connector_voltage_drop():
    assert connector_voltage_drop(
        total_current_a=6.0,
        contact_resistance_mohm=10,
        number_of_parallel_pins=4,
    ) == pytest.approx(0.015)


def test_connector_power_loss():
    assert connector_power_loss(
        total_current_a=6.0,
        contact_resistance_mohm=10,
        number_of_parallel_pins=4,
    ) == pytest.approx(0.09)


def test_is_current_within_connector_rating_true():
    assert is_current_within_connector_rating(
        total_current_a=6.0,
        number_of_pins=4,
        rated_current_per_pin_a=2.0,
        derating_factor=0.8,
    ) is True


def test_is_current_within_connector_rating_false():
    assert is_current_within_connector_rating(
        total_current_a=7.0,
        number_of_pins=4,
        rated_current_per_pin_a=2.0,
        derating_factor=0.8,
    ) is False
