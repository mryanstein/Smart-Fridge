import pytest

from fridge_manager.domain.quantity import Unit, Kind
from fridge_manager.domain.errors import IncompatibleUnitError, InvalidQuantityError, InvalidUnitError


def test_unit_kind():
    assert Unit.KG.kind == Kind.MASS
    assert Unit.L.kind == Kind.VOLUME
    assert Unit.PCS.kind == Kind.COUNT


def test_kg_to_g():
    assert Unit.KG.convert(2, Unit.G) == 2000


def test_g_to_kg():
    assert Unit.G.convert(500, Unit.KG) == 0.5


def test_l_to_ml():
    assert Unit.L.convert(1.5, Unit.ML) == 1500


def test_ml_to_l():
    assert Unit.ML.convert(250, Unit.L) == 0.25


def test_pieces():
    assert Unit.PCS.convert(3, Unit.PCS) == 3


def test_same_unit():
    assert Unit.KG.convert(2, Unit.KG) == 2


def test_zero_amount():
    assert Unit.G.convert(0, Unit.KG) == 0


def test_incompatible_units():
    with pytest.raises(IncompatibleUnitError):
        Unit.KG.convert(2, Unit.L)


def test_negative_amount():
    with pytest.raises(InvalidQuantityError):
        Unit.KG.convert(-2, Unit.G)


def test_invalid_string_amount():
    with pytest.raises(InvalidQuantityError):
        Unit.KG.convert("abc", Unit.G)


def test_none_amount():
    with pytest.raises(InvalidQuantityError):
        Unit.KG.convert(None, Unit.G)


def test_boolean_amount():
    with pytest.raises(InvalidQuantityError):
        Unit.KG.convert(True, Unit.G)


def test_invalid_target():
    with pytest.raises(InvalidUnitError):
        Unit.KG.convert(2, "G")


def test_fractional_conversion():
    result = Unit.L.convert(0.3, Unit.ML)
    assert result == pytest.approx(300)
