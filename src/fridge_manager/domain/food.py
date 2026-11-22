from abc import ABC, abstractmethod
from .quantity import Unit, Kind


#potem można rozszerzyć funckjonalność np. kalkulator kalorii
class FoodItem(ABC):
    def __init__(self, name: str, stock_unit: Unit) -> None:
        self._name = name.strip()
        self._stock_unit = stock_unit   #w jakiej jednostce bazowej przechowywany/kupowany jest produkt np. mleko w l nie ml

    #TODO sprawdzić czy nazwa nie jest pusta, czy napewno stock_unit jest elementen unit (dorobić ValueError, TypeError)

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

#TODO: trzy klasy pochodne: jak przeliczyć ilość na bazową i na gramy (abstractmethod: to_grams)
class WeightItem(FoodItem):
    pass


class VolumeItem(FoodItem):
    pass


class PieceItem(FoodItem):
    pass
