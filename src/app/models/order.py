from typing import Any, Dict, List, Optional, Self, TypedDict

from app.models.dish import Dish
from app.models.model_protocol import Modelable
from app.sqlite import SQLite


class OrderForm(TypedDict):
    id: Optional[int]
    bill_id: int
    is_healthy: int


class Order(Modelable):
    _db = SQLite()

    def __init__(self) -> None:
        super().__init__()
        self.id = 0
        self.bill_id = 0

    def with_id(self: Self, id: int) -> Self:
        self.id = int(id)
        return self

    def with_bill_id(self: Self, bill_id: int) -> Self:
        self.bill_id = int(bill_id)
        return self

    def with_is_healthy(self: Self, is_healthy: int) -> Self:
        self.is_healthy = int(is_healthy)
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
        for key, value in form.items():
            setattr(res, key, value)
        return res

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
        cur = Order._db.execute(
            "INSERT INTO Orders (bill_id) VALUES (?)", [self.bill_id]
        )
        if cur.lastrowid:
            self.id = cur.lastrowid
        Order._db.connection.commit()

    def save(self: Self) -> None:
        Order._db.execute(
            "UPDATE Orders SET bill_id = ? WHERE id = ?",
            [self.bill_id, self.id],
        )

    def to_dict(self: Self) -> Dict:
        return {"id": self.id, "bill_id": self.bill_id}

    @property
    def dishes(self: Self) -> List[Dish]:
        cur = Order._db.execute(
            "SELECT di.id, di.name, di.type From Dishes_Orders as d JOIN Dishes as di ON d.dish_id = di.id WHERE order_id = ?",
            [self.id],
        )
        return Dish.from_rows(cur.fetchall())
