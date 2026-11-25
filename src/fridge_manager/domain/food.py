from abc import ABC, abstractmethod
from .quantity import Unit, Kind
from .errors import InvalidProductNameError, InvalidUnitError, IncompatibleUnitError, InvalidQuantityError


#potem można rozszerzyć funckjonalność np. kalkulator kalorii
class FoodItem(ABC):
    def __init__(self, name: str, stock_unit: Unit) -> None:
        if not isinstance(name, str) or not name.strip():
            raise InvalidProductNameError("Nieprawidłowa nazwa produktu")

        if not isinstance(stock_unit, Unit):
            raise InvalidUnitError("Nieprawidłowa jednostka produktu")

        self._name = name.strip()
        self._stock_unit = stock_unit   #w jakiej jednostce bazowej przechowywany/kupowany jest produkt np. mleko w l nie ml

    @property
    def name(self) -> str:
        return self._name

    @property
    def stock_unit(self) -> Unit:
        return self._stock_unit

    @property
    def kind(self) -> Kind:
        return self.stock_unit.kind

    def convert(self, amount: float, target: Unit) -> float:
        return self.stock_unit.convert(amount, target)  #z stock_unit na dowolna

    def to_stock_unit(self, amount: float, unit: Unit) -> float:
        return unit.convert(amount, self.stock_unit)  #z dowolnej na stock_unit

    @abstractmethod
    def to_grams(self, amount: float, unit: Unit) -> float:
        pass

class WeightItem(FoodItem):
    def __init__(self, name, stock_unit):
        super().__init__(name, stock_unit)
        if self.kind != Kind.MASS:
            raise IncompatibleUnitError(
                "WeightItem wymaga jednostki masy"
            )

    def to_grams(self, amount: float, unit: Unit) -> float:
        return unit.convert(amount, Unit.G)


class VolumeItem(FoodItem):
    def __init__(self, name, stock_unit, grams_per_ml):
        super().__init__(name, stock_unit)
        self._grams_per_ml = grams_per_ml
        if not isinstance(grams_per_ml, (int, float)) or not grams_per_ml>0:
            raise InvalidQuantityError(
                "grams_per_piece musi być dodatnią liczbą"
            )
        if self.kind != Kind.VOLUME:
            raise IncompatibleUnitError(
                "VolumeItem wymaga jednostki pbjętości"
            )

    def to_grams(self, amount: float, unit: Unit) -> float:
        ml = unit.convert(amount, Unit.ML)
        return ml * self._grams_per_ml


class PieceItem(FoodItem):
    def __init__(self, name, stock_unit, grams_per_piece):
        super().__init__(name, stock_unit)
        if not isinstance(grams_per_piece, (int, float)) or not grams_per_piece>0:
            raise InvalidQuantityError(
                "grams_per_piece musi być dodatnią liczbą"
            )
        if self.kind != Kind.COUNT:
            raise IncompatibleUnitError(
                "PieceItem wymaga produktu w sztukach"
            )

        self._grams_per_piece = grams_per_piece

    def to_grams(self, amount: float, unit: Unit) -> float:
        pieces = unit.convert(amount, Unit.PCS)
        return pieces * self._grams_per_piece

