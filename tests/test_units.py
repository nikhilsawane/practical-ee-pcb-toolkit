import pytest

from ee_pcb_toolkit.units import mil_to_mm, mm_to_mil, copper_oz_to_um


def test_mil_to_mm():
    assert mil_to_mm(10) == pytest.approx(0.254)


def test_mm_to_mil():
    assert mm_to_mil(0.254) == pytest.approx(10)


def test_copper_oz_to_um():
    assert copper_oz_to_um(1) == pytest.approx(34.8)
