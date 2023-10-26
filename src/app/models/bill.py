from sqlite3 import Error
from typing import Any, Self, List, TypedDict, Optional, Dict
from datetime import datetime
from app.models.model_protocol import Modelable
from app.models.order import Order
from app.sqlite import SQLite


class BillForm(TypedDict):
    id: Optional[int]
    total: float
    date_time: datetime
    type: int
    table_id: int


class Bill(Modelable):
    _db = SQLite()

    def __init__(self: Self) -> None:
        super().__init__()
        self.id = 0
        self.total = 0.0
        self.date_time: datetime = datetime.now()
        self.type = 0
        self.table_id = 0

    def with_id(self: Self, id: int) -> Self:
        self.id = int(id)
        return self

    def with_total(self: Self, total: float) -> Self:
        self.total = float(total)
        return self

    def with_date_time(self: Self, date_time: datetime) -> Self:
        self.date_time = date_time 
        return self

    def with_type(self: Self, _type: int) -> Self:
        self.type = int(_type)
        return self

    def with_table_id(self: Self, table_id: int) -> Self:
        self.table_id = int(table_id)
        return self

    @classmethod
    def from_row(cls, row: List[Any]) -> Self:
        id, total, date_time, _type, table_id = row
        return (
            cls()
            .with_id(id)
            .with_total(total)
            .with_date_time(date_time)
            .with_type(_type)
            .with_table_id(table_id)
        )

    @classmethod
    def from_rows(cls, rows: List[List[Any]]) -> List[Self]:
        return [cls.from_row(row) for row in rows]

    @classmethod
    def from_form(cls, form: BillForm) -> Self:
        res = cls()
        for key, value in form.items():
            setattr(res, key, value)
        return res

    def to_dict(self: Self) -> Dict:
        return {
            "id": self.id,
            "total": self.total,
            "date_time": self.date_time,
            "type": self.type,
            "table_id": self.table_id,
        }

    @classmethod
    def all(cls) -> List[Self]:
        cur = cls._db.execute("SELECT * FROM Bills")
        return cls.from_rows(cur.fetchall())

    @classmethod
    def find(cls, id: int) -> Optional[Self]:
        cur = cls._db.execute("SELECT * FROM Bills WHERE id = ?", [id])
        row = cur.fetchone()
        if row is None:
            return None
        return Bill.from_row(row)

    def save(self: Self) -> None:
        Bill._db.execute(
            "UPDATE Bills SET total = ?, date_time = ?, type = ?, table_id = ? WHERE id = ?",
            [self.total, self.date_time, self.type, self.table_id, self.id],
        )
        Bill._db.connection.commit()

    def store(self: Self) -> None:
        if self.id != 0:
            raise Error("That record already exists!")
        cur = Bill._db.execute(
            "INSERT INTO Bills (total, date_time, type, table_id) VALUES (?, ?, ?, ?)",
            [self.total, self.date_time, self.type, self.table_id],
        )
        if cur.lastrowid:
            self.id = cur.lastrowid
        Bill._db.connection.commit()

    @property
    def orders(self: Self) -> List[Order]:
        cur = Bill._db.execute("SELECT * FROM Orders WHERE bill_id = ?", [self.id])
        return Order.from_rows(cur.fetchall())
