from typing import Any, List, Self, TypedDict, Optional, Dict
from enum import IntEnum, auto
from app.models.model_protocol import Modelable


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


class FoodForm(TypedDict):
    id: Optional[int]
    type: int
    subtype: int
    name: str
    calories: float
    price: float


# XXX: This POS uses the builder design pattern
class Food(Modelable):
    def __init__(self: Self) -> None:
        self.id = 0
        # XXX: Default id, this must be autoincremented or
        # populated from the database
        self.type = 0
        self.subtype = 0
        self.name = ""
        self.calories = 0.0
        self.price = 0.0

    def __str__(self: Self) -> str:
        return f"Food({self.name})"

    def to_dict(self: Self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "subtype": self.subtype,
            "name": self.name,
            "calories": self.calories,
            "price": self.price,
        }

    @property
    def values(self: Self, with_id=False) -> List:
        if with_id:
            return [self.id, self.type, self.subtype, self.name, self.calories, self.price]
        return [self.type, self.subtype, self.name, self.calories, self.price]

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

    def with_price(self: Self, price: float) -> Self:
        self.price = price
        return self

    @staticmethod
    def from_form(form: FoodForm) -> "Food":
        res = Food()
        for key, value in form:
            setattr(res, key, value)
        return res

    @staticmethod
    def from_row(row: List[Any]) -> "Food":
        id, _type, subtype, name, calories, price = row
        res = (
            Food()
            .with_id(id)
            .with_type(_type)
            .with_subtype(subtype)
            .with_name(name)
            .with_calories(calories)
            .with_price(price)
        )
        return res

    @staticmethod
    def from_rows(rows: List[List[Any]]) -> List:
        return [Food.from_row(row) for row in rows]
