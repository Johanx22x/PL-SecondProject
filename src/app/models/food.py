from enum import IntEnum, auto
from sqlite3 import Error
from typing import Any, Dict, List, Optional, Self, TypedDict
from app.prolog import Prolog

from app.models.model_protocol import Modelable
from app.sqlite import SQLite


class FoodType(IntEnum):
    DRINK = auto()
    PROTEIN = auto()
    SIDE_DISH = auto()
    DESSERT = auto()


class FoodSubType(IntEnum):
    SODA = auto()  # Drink
    NATURAL = auto()
    WATER_BASED = auto()
    MILK_BASED = auto()
    HOT = auto()  # Drinks & Side Dishes
    COLD = auto()
    RED_MEAT = auto()  # Proteins
    CHICKEN = auto()
    FISH = auto()
    SEAFOOD = auto()
    VEGETABLES = auto()  # Side Dishes
    CARBS = auto()
    LACTOSE = auto()  # Desserts
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
    _db = SQLite()

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
        return f'food({self.type}, {self.subtype}, "{self.name}", {self.calories}, {self.price}).'

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
            return [
                self.id,
                self.type,
                self.subtype,
                self.name,
                self.calories,
                self.price,
            ]
        return [self.type, self.subtype, self.name, self.calories, self.price]

    def with_id(self: Self, id: int) -> Self:
        self.id = int(id)
        return self

    def with_type(self: Self, _type: FoodType) -> Self:
        self.type = int(_type)
        return self

    def with_subtype(self: Self, subtype: FoodSubType) -> Self:
        self.subtype = int(subtype)
        return self

    def with_name(self: Self, name: str) -> Self:
        self.name = name
        return self

    def with_calories(self: Self, calories: float) -> Self:
        self.calories = float(calories)
        return self

    def with_price(self: Self, price: float) -> Self:
        self.price = float(price)
        return self

    @classmethod
    def from_form(cls, form: FoodForm) -> Self:
        res = cls()
        print(form)

        for key, value in form.items():
            setattr(res, key, value)
        return res

    @classmethod
    def from_row(cls, row: List[Any]) -> Self:
        id, _type, subtype, name, calories, price = row
        res = (
            cls()
            .with_id(id)
            .with_type(_type)
            .with_subtype(subtype)
            .with_name(name)
            .with_calories(calories)
            .with_price(price)
        )
        return res

    @classmethod
    def from_rows(cls, rows: List[List[Any]]) -> List[Self]:
        return [Food.from_row(row) for row in rows]

    @classmethod
    def all(cls) -> List[Self]:
        cur = cls._db.execute("SELECT * FROM Foods")
        return cls.from_rows(cur.fetchall())

    @classmethod
    def find(cls, id: int) -> Optional[Self]:
        cur = cls._db.execute("SELECT * FROM Foods WHERE id = ?", [id])
        row = cur.fetchone()
        if row is None:
            return None
        return Food.from_row(row)

    def store(self: Self) -> None:
        if self.id != 0:
            raise Error("That record already exists!")
        cur = Food._db.execute(
            "INSERT INTO Foods (type, subtype, name, calories, price) VALUES (?, ?, ?, ?, ?)",
            [self.type, self.subtype, self.name, self.calories, self.price],
        )
        if cur.lastrowid:
            self.id = cur.lastrowid
        Food._db.connection.commit()

        try:
            prolog = Prolog()
            prolog.query(f"assertz(food({self.type}, {self.subtype}, '{self.name}', {self.calories}, {self.price})).")
        except Exception as e:
            print(e)

    def save(self: Self) -> None:
        Food._db.execute(
            "UPDATE Foods SET type = ?, subtype = ?, name = ?, calories = ?, price = ? WHERE id = ?",
            [
                self.type,
                self.subtype,
                self.name,
                self.calories,
                self.price,
                self.id,
            ],
        )
        Food._db.connection.commit()

    def delete(self: Self) -> None:
        Food._db.execute(
            "DELETE FROM Foods WHERE id = ?",
            [self.id],
        )
        Food._db.connection.commit()

        try:
            prolog = Prolog()
            prolog.query(f"retract(food({self.type}, {self.subtype}, '{self.name}', {self.calories}, {self.price})).")
        except Exception as e:
            print(e)
