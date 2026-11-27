import pytest

from fridge_manager.domain.food import VolumeItem
from fridge_manager.domain.fridge import Fridge
from fridge_manager.domain.quantity import Unit


def test_add_converts_to_product_stock_unit():
    fridge = Fridge()
    milk = VolumeItem("Mleko", Unit.L, 1.03)

    fridge.add(milk, 300, Unit.ML)

    assert fridge.available(milk) == pytest.approx(0.3)