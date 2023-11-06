from sqlite3 import Error
from typing import Any, Dict, List, Optional, Self, TypedDict

from app.models.dish import Dish
from app.models.model_protocol import Modelable
from app.sqlite import SQLite


class OrderForm(TypedDict):
    id: Optional[int]
    bill_id: int


class Order(Modelable):
    _db = SQLite()

    def __init__(self) -> None:
        super().__init__()
        self.id = 0
        self.bill_id = 0
        self._dishes = []

    def with_id(self: Self, id: int) -> Self:
        self.id = int(id)
        return self

    def with_bill_id(self: Self, bill_id: int) -> Self:
        self.bill_id = int(bill_id)
        return self

    @classmethod
    def from_row(cls, row: List[Any]) -> Self:
        id, bill_id = row
        return cls().with_id(id).with_bill_id(bill_id)

    @classmethod
    def from_rows(cls, rows: List[List[Any]]) -> List[Self]:
        return [cls.from_row(row) for row in rows]

    @classmethod
    def from_form(cls, form: OrderForm) -> Self:
        res = cls()
        for key, value in filter(
                lambda entry: entry[0] != "dishes", form.items()
        ):
            setattr(res, key, value)

        if dishes := form.get("dishes"):
            res._dishes = dishes

        return res

    def save_dish(self: Self, dish_id: int) -> None:
        Dish._db.execute(
            "INSERT INTO Dishes_Orders (dish_id, order_id) VALUES (?, ?)",
            [dish_id, self.id],
        )
        Dish._db.connection.commit()

    @classmethod
    def all(cls) -> List[Self]:
        cur = cls._db.execute("SELECT * FROM Orders")
        return Order.from_rows(cur.fetchall())

    @classmethod
    def find(cls, id: int) -> Optional[Self]:
        cur = cls._db.execute("SELECT * FROM Orders WHERE id = ?", [id])
        row = cur.fetchone()
        if row is None:
            return None
        return cls.from_row(row)

    def store(self: Self) -> None:
        if self.id != 0:
            raise Error("That record already exists!")
        cur = Order._db.execute(
            "INSERT INTO Orders (bill_id) VALUES (?)", [self.bill_id]
        )
        if cur.lastrowid:
            self.id = cur.lastrowid
        Order._db.connection.commit()

        for dish in self._dishes:
            self.save_dish(dish["id"])

    def save(self: Self) -> None:
        Order._db.execute(
            "UPDATE Orders SET bill_id = ? WHERE id = ?",
            [self.bill_id, self.id],
        )
        
        cur = Order._db.execute(
            "SELECT * FROM Dishes_Orders WHERE order_id = ?", [self.id]
        )

        dishes = map(lambda d: d["id"], self._dishes)
        values = map(lambda v: v[0], cur.fetchall())
        to_add = filter(lambda d: d not in values, dishes)
        to_delete = filter(lambda v: v not in dishes, values)

        for dish in to_add:
            Dish._db.execute(
                "INSERT INTO Dishes_Orders (dish_id, order_id) VALUES (?, ?)",
                [dish, self.id],
            )

        for dish in to_delete:
            Dish._db.execute(
                "DELETE FROM Dishes_Orders WHERE order_id = ? AND dish_id = ?",
                [self.id, dish],
            )

        Order._db.connection.commit()

    def to_dict(self: Self) -> Dict:
        return {"id": self.id, "bill_id": self.bill_id, "dishes": [dish.to_dict() for dish in self.dishes]}

    @property
    def dishes(self: Self) -> List[Dish]:
        cur = Order._db.execute(
            "SELECT di.id, di.name, di.type, di.is_predef From Dishes_Orders as d JOIN Dishes as di ON d.dish_id = di.id WHERE order_id = ?",
            [self.id],
        )
        return Dish.from_rows(cur.fetchall())
