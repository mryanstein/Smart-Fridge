#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum

class Kind(Enum):
    MASS = "masa"
    VOLUME = "objetosc"
    COUT = "ilosc"

class Unit(Enum):
    G = (Kind.MASS, 1)
    KG = (Kind.MASS, 1000)

    ML = (Kind.VOLUME, 1)
    L = (Kind.VOLUME, 1000)

    PSC = (Kind.COUT, 1)

    def __init__(self, kind_, factor_):
        self.kind = kind_                   #KIND.MASS
        self.factor = factor_               #1000

    def convert(self, amount: float, target: Unit) -> float:
        #dodać wyjątki - amount<0, self.kind != target.kind
        return amount * self.factor / target.factor

#napisać testy



