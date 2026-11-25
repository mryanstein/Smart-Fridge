
import pytest

from fridge_manager.domain.food import FoodItem, WeightItem, VolumeItem, PieceItem
from fridge_manager.domain.quantity import Unit, Kind
from fridge_manager.domain.errors import InvalidProductNameError, InvalidUnitError, InvalidQuantityError, IncompatibleUnitError


def test_abstract_food_item():
    with pytest.raises(TypeError):
        FoodItem("Produkt", Unit.KG)


def test_weight_item():
    product = WeightItem("Makaron", Unit.KG)

    assert product.name == "Makaron"
    assert product.kind == Kind.MASS
    assert product.stock_unit == Unit.KG


def test_volume_item():
    product = VolumeItem("Mleko", Unit.L, 1.03)

    assert product.name == "Mleko"
    assert product.kind == Kind.VOLUME


def test_piece_item():
    product = PieceItem("Jajko", Unit.PCS, 60)

    assert product.name == "Jajko"
    assert product.kind == Kind.COUNT


def test_to_stock_unit():
    product = VolumeItem("Mleko", Unit.L, 1.03)

    result = product.to_stock_unit(300, Unit.ML)

    assert result == pytest.approx(0.3)


def test_convert_from_stock_unit():
    product = WeightItem("Makaron", Unit.KG)

    assert product.convert(2, Unit.G) == 2000


def test_weight_to_grams():
    product = WeightItem("Makaron", Unit.KG)

    assert product.to_grams(0.5, Unit.KG) == 500


def test_volume_to_grams():
    product = VolumeItem("Mleko", Unit.L, 1.03)

    assert product.to_grams(1, Unit.L) == pytest.approx(1030)


def test_piece_to_grams():
    product = PieceItem("Jajko", Unit.PCS, 60)

    assert product.to_grams(3, Unit.PCS) == 180


def test_empty_product_name():
    with pytest.raises(InvalidProductNameError):
        WeightItem("", Unit.KG)


def test_whitespace_product_name():
    with pytest.raises(InvalidProductNameError):
        WeightItem("   ", Unit.KG)


def test_none_product_name():
    with pytest.raises(InvalidProductNameError):
        WeightItem(None, Unit.KG)


def test_numeric_product_name():
    with pytest.raises(InvalidProductNameError):
        WeightItem(123, Unit.KG)


def test_invalid_stock_unit():
    with pytest.raises(InvalidUnitError):
        WeightItem("Makaron", "KG")


def test_wrong_unit_for_weight_item():
    with pytest.raises(IncompatibleUnitError):
        WeightItem("Makaron", Unit.L)


def test_wrong_unit_for_volume_item():
    with pytest.raises(IncompatibleUnitError):
        VolumeItem("Mleko", Unit.KG, 1.03)


def test_invalid_density():
    with pytest.raises(InvalidQuantityError):
        VolumeItem("Mleko", Unit.L, -1)


def test_invalid_piece_weight():
    with pytest.raises(InvalidQuantityError):
        PieceItem("Jajko", Unit.PCS, 0)


def test_polymorphism():
    products = [
        (WeightItem("Makaron", Unit.KG), 1, Unit.KG, 1000),
        (VolumeItem("Mleko", Unit.L, 1.03), 1, Unit.L, 1030),
        (PieceItem("Jajko", Unit.PCS, 60), 2, Unit.PCS, 120)
    ]

    for product, amount, unit, expected in products:
        assert isinstance(product, FoodItem)
        assert product.to_grams(amount, unit) == pytest.approx(expected)


def test_read_only_properties():
    product = WeightItem("Makaron", Unit.KG)

    with pytest.raises(AttributeError):
        product.name = "Ryż"

    with pytest.raises(AttributeError):
        product.stock_unit = Unit.G
