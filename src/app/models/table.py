from sqlite3 import Error
from typing import Any, Dict, List, Optional, Self, TypedDict

from app.models.bill import Bill
from app.models.model_protocol import Modelable
from app.sqlite import SQLite


class TableForm(TypedDict):
    id: Optional[int]
    name: str
    people: int


class Table(Modelable):
    _db = SQLite()

    def __init__(self) -> None:
        super().__init__()
        self.id = 0
        self.name = ""
        self.people = 0

    def with_id(self: Self, id: int) -> Self:
        self.id = int(id)
        return self

    def with_name(self: Self, name: str) -> Self:
        self.name = name
        return self

    def with_people(self: Self, people: int) -> Self:
        self.people = int(people)
        return self

    @classmethod
    def from_row(cls, row: List[Any]) -> Self:
        id, name, people = row
        return cls().with_id(id).with_name(name).with_people(people)

    @classmethod
    def from_rows(cls, rows: List[List[Any]]) -> List[Self]:
        return [cls.from_row(row) for row in rows]

    @classmethod
    def from_form(cls, form: TableForm) -> Self:
        return cls().with_name(form["name"]).with_people(form["people"])

    def to_dict(self: Self) -> Dict:
        return {"id": self.id, "name": self.name, "people": self.people}

    @classmethod
    def all(cls) -> List[Self]:
        cur = cls._db.execute("SELECT * FROM Tables")
        return Table.from_rows(cur.fetchall())

    @classmethod
    def find(cls, id: int) -> Optional[Self]:
        cur = cls._db.execute("SELECT * FROM Tables WHERE id = ?", [id])
        row = cur.fetchone()
        if row is None:
            return None
        return Table.from_row(row)

    def store(self: Self) -> None:
        if self.id != 0:
            raise Error("That record already exists!")
        cur = Table._db.execute(
            "INSERT INTO Tables (name, people) VALUES (?, ?)",
            [self.name, self.people],
        )
        if cur.lastrowid:
            self.id = cur.lastrowid
        Table._db.connection.commit()

    def save(self: Self) -> None:
        Table._db.execute(
            "UPDATE Tables SET name = ?, people = ? WHERE id = ?",
            [self.name, self.people, self.id],
        )

    def delete(self: Self) -> None:
        Table._db.execute("DELETE FROM Tables WHERE id = ?", [self.id])

    @property
    def bills(self: Self) -> List[Bill]:
        cur = Table._db.execute(
            "SELECT * FROM Bills WHERE table_id = ?", [self.id]
        )
        return Bill.from_rows(cur.fetchall())
