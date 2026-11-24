from enum import Enum
from .errors import IncompatibleUnitError, InvalidQuantityError, InvalidUnitError

class Kind(Enum):
    MASS = "masa"
    VOLUME = "objetosc"
    COUNT = "ilosc"

class Unit(Enum):
    G = (Kind.MASS, 1)
    KG = (Kind.MASS, 1000)

    ML = (Kind.VOLUME, 1)
    L = (Kind.VOLUME, 1000)

    PCS = (Kind.COUNT, 1)

    def __init__(self, kind, factor):
        self._kind = kind                   #KIND.MASS
        self._factor = factor               #1000

    @property
    def kind(self) -> Kind:
        return self._kind

    @property
    def factor(self) -> float:
        return self._factor

    def convert(self, amount: float, target: "Unit") -> float:
        if amount < 0:
            raise InvalidQuantityError("Ilość nie może być ujemna")

        if not isinstance(target, Unit):
            raise InvalidUnitError("Nieprawidłowa jednostka docelowa")

        if self._kind != target._kind:
            raise IncompatibleUnitError(f"Nie można przeliczyć {self.name} na {target.name}")

        return amount * self._factor / target._factor

#TODO napisać testy



