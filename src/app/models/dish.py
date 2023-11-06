from sqlite3 import Error
from typing import Any, Dict, List, Optional, Self, TypedDict

from app.models.food import Food
from app.models.model_protocol import Modelable
from app.sqlite import SQLite


class DishForm(TypedDict):
    id: Optional[int]
    name: str
    type: int
    foods: Optional[List[int]]


class Dish(Modelable):
    _db = SQLite()

    def __init__(self: Self) -> None:
        self.id = 0
        self.name = ""
        self.type = 0
        self.is_predef = 1
        self._foods = []

    def __str__(self: Self) -> str:
        return f'dish("{self.name}", {self.type}).'

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "predef": bool(self.is_predef),
            "foods": [food.to_dict() for food in self.foods],
        }

    def with_id(self: Self, id: int) -> Self:
        self.id = int(id)
        return self

    def with_name(self: Self, name: str) -> Self:
        self.name = name
        return self

    def with_type(self: Self, _type: int) -> Self:
        self.type = int(_type)
        return self

    def with_predef(self: Self, predef: int) -> Self:
        self.is_predef = predef
        return self

    @classmethod
    def from_form(cls, form: DishForm) -> Self:
        res = cls()
        for key, value in filter(
            lambda entry: entry[0] != "foods", form.items()
        ):
            setattr(res, key, value)

        if foods := form.get("foods"):
            res._foods = foods

        return res

    def save_food(self: Self, food_id: int):
        Food._db.execute(
            "INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (?, ?)",
            [self.id, food_id],
        )
        Food._db.connection.commit()

    @classmethod
    def from_row(cls, row: List[Any]) -> Self:
        id, name, _type, is_predef = row
        return (
            cls()
            .with_id(id)
            .with_name(name)
            .with_type(_type)
            .with_predef(is_predef)
        )

    @classmethod
    def from_rows(cls, rows: List[List[Any]]) -> List[Self]:
        return [cls.from_row(row) for row in rows]

    @classmethod
    def all(cls) -> List[Self]:
        cur = cls._db.execute("SELECT * FROM Dishes")
        res = cls.from_rows(cur.fetchall())
        return res

    def delete(self: Self) -> None:
        Food._db.execute(
            "DELETE FROM Dishes WHERE id = ?",
            [self.id],
        )
        Food._db.connection.commit()

    @classmethod
    def find(cls, id: int) -> Optional[Self]:
        cur = cls._db.execute("SELECT * From Dishes WHERE id = ?", [id])
        row = cur.fetchone()
        if row is None:
            return None
        return Dish.from_row(row)

    def store(self: Self) -> None:
        if self.id != 0:
            raise Error("That record already exists!")
        cur = Dish._db.execute(
            "INSERT INTO Dishes (name, is_predef) VALUES (?, ?)",
            [self.name, self.is_predef],
        )
        if cur.lastrowid:
            self.id = cur.lastrowid
        Dish._db.connection.commit()
        for food in self._foods:
            self.save_food(food["id"])

    def save(self: Self) -> None:
        Dish._db.execute(
            "UPDATE Dishes SET name = ?, type = ? WHERE id = ?",
            [self.name, self.type, self.id],
        )

        cur = Dish._db.execute(
            "SELECT food_id FROM Dishes_Foods WHERE dish_id = ?", [self.id]
        )

        foods = map(lambda f: f["id"], self._foods)
        values = map(lambda v: v[0], cur.fetchall())
        to_add = filter(lambda f: f not in values, foods)
        to_delete = filter(lambda v: v not in foods, values)

        for food_id in to_delete:
            Dish._db.execute(
                "DELETE FROM Dishes_Foods WHERE food_id = ?", [food_id]
            )

        for food_id in to_add:
            Dish._db.execute(
                "INSERT INTO Dishes_Foods (dish_id, food_id) VALUES (?, ?)",
                [self.id, food_id],
            )

        Dish._db.connection.commit()

    @property
    def foods(self: Self) -> List[Food]:
        cur = Dish._db.execute(
            "SELECT f.id, f.type, f.subtype, f.name, f.calories, f.price FROM Dishes_Foods as df JOIN Foods as f ON f.id = df.food_id WHERE df.dish_id = ?",
            [self.id],
        )
        return Food.from_rows(cur.fetchall())
