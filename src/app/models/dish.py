from typing import Self, TypedDict, Optional, Any, List, Dict
from app.models.model_protocol import Modelable


class DishForm(TypedDict):
    id: Optional[int]
    name: str
    type: int


class Dish(Modelable):
    def __init__(self: Self) -> None:
        self.id = 0
        self.name = ""
        self.type = 0

    @property
    def values(self, with_id=False):
        if with_id:
            return [self.id, self.name, self.type]
        return [self.name, self.type]

    def to_dict(self) -> Dict:
        return {"id": self.id, "name": self.name, "type": self.type}

    def with_id(self: Self, id: int) -> Self:
        self.id = id
        return self

    def with_name(self: Self, name: str) -> Self:
        self.name = name
        return self

    def with_type(self: Self, _type: int) -> Self:
        self.type = _type
        return self

    @staticmethod
    def from_form(form: DishForm) -> "Dish":
        res = Dish()
        for key, value in form:
            setattr(res, key, value)
        return res

    @staticmethod
    def from_row(row: List[Any]):
        id, name, _type = row
        return Dish().with_id(id).with_name(name).with_type(_type)

    @staticmethod
    def from_rows(rows: List[List[Any]]) -> List:
        return [Dish.from_row(row) for row in rows]
