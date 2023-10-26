from sqlite3 import Error
from typing import Self, TypedDict, Optional, Any, List, Dict
from app.models.food import Food
from app.models.model_protocol import Modelable
from app.sqlite import SQLite


class DishForm(TypedDict):
    id: Optional[int]
    name: str
    type: int


class Dish(Modelable):
    _db = SQLite()

    def __init__(self: Self) -> None:
        self.id = 0
        self.name = ""
        self.type = 0

    def __str__(self: Self) -> str:
        return f'dish("{self.name}", {self.type}).'

    def to_dict(self) -> Dict:
        return {"id": self.id, "name": self.name, "type": self.type}

    def with_id(self: Self, id: int) -> Self:
        self.id = int(id)
        return self

    def with_name(self: Self, name: str) -> Self:
        self.name = name
        return self

    def with_type(self: Self, _type: int) -> Self:
        self.type = int(_type)
        return self

    @classmethod
    def from_form(cls, form: DishForm) -> Self:
        res = cls()
        for key, value in form.items():
            setattr(res, key, value)
        return res

    @classmethod
    def from_row(cls, row: List[Any]) -> Self:
        id, name, _type = row
        return cls().with_id(id).with_name(name).with_type(_type)

    @classmethod
    def from_rows(cls, rows: List[List[Any]]) -> List[Self]:
        return [cls.from_row(row) for row in rows]

    @classmethod
    def all(cls) -> List[Self]:
        cur = cls._db.execute("SELECT * FROM Dishes")
        res = cls.from_rows(cur.fetchall())
        return res

    @classmethod
    def find(cls, id: int) -> Optional[Self]:
        cur = cls._db.execute("SELECT * From foods WHERE id = ?", [id])
        row = cur.fetchone()
        if row is None:
            return None
        return Dish.from_row(row)

    def store(self: Self) -> None:
        if self.id != 0:
            raise Error("That record already exists!")
        cur = Dish._db.execute(
            "INSERT INTO Dishes (name, type) VALUES (?, ?)", [self.name, self.type]
        )
        if cur.lastrowid:
            self.id = cur.lastrowid
        Dish._db.connection.commit()

    def save(self: Self) -> None:
        Dish._db.execute(
            "UPDATE Dishes SET name = ?, type = ? WHERE id = ?", [self.name, self.type, self.id]
        )
        Dish._db.connection.commit()

    @property
    def foods(self: Self) -> List[Food]:
        cur = Dish._db.execute(
            "SELECT f.id, f.type, f.subtype, f.name, f.calories, f.price FROM Dishes_Foods as df JOIN Foods as f ON f.id = df.food_id WHERE df.dish_id = ?",
            [self.id],
        )
        return Food.from_rows(cur.fetchall())
