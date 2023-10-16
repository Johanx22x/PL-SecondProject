from typing import Self
from enum import IntEnum, auto

class FoodType(IntEnum):
    DRINK = auto()
    PROTEIN = auto()
    SIDE_DISH = auto()
    DESSERT = auto()

class FoodSubType(IntEnum):
    SODA = auto()

    NATURAL = auto()
    WATER_BASED = auto()
    MILK_BASED = auto()

    HOT = auto()
    COLD = auto()

    RED_MEAT = auto()
    CHICKEN = auto()
    FISH = auto()
    SEAFOOD = auto()

    VEGETABLES = auto()
    CARBS = auto()

    LACTOSE = auto()
    NO_LACTOSE = auto()
    FRUIT = auto()


# XXX: This POS uses the builder design pattern
class Food:
    def __init__(self: Self) -> None:
        self.id = 0 # XXX: Default id, this must be autoincremented or
                    # populated from the database
        self.type = 0
        self.subtype = 0
        self.name = ""
        self.calories = 0.0

    def __str__(self: Self) -> str:
        return f"Food({self.name})"

    def with_id(self: Self, id: int) -> Self:
        self.id = id
        return self

    def with_type(self: Self, _type: FoodType) -> Self:
        self.type = _type
        return self
    
    def with_subtype(self: Self, subtype: FoodSubType) -> Self:
        self.subtype = subtype
        return self

    def with_name(self: Self, name: str) -> Self:
        self.name = name
        return self

    def with_calories(self: Self, calories: float) -> Self:
        self.calories = calories
        return self
