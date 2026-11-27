from .food import FoodItem
from .quantity import Unit


class Fridge:
    def __init__(self) -> None:
        self._items: dict[str, float] = {}

    def add(self, food: FoodItem, amount: float, unit: Unit) -> None:
        amount_in_stock_unit = food.to_stock_unit(amount, unit)
        key = food.name.casefold()
        self._items[key] = self._items.get(key, 0.0) + amount_in_stock_unit

    def available(self, food: FoodItem) -> float:
        return self._items.get(food.name.casefold(), 0.0)