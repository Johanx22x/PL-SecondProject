from typing import Protocol, List, Any, Dict, Self


class Modelable(Protocol):
    @classmethod
    def from_row(cls, row: List[Any]) -> Self:
        ...

    @classmethod
    def from_rows(cls, rows: List[List[Any]]) -> List[Self]:
        ...

    @classmethod
    def from_form(cls, form: Dict) -> Self:
        ...

    def to_dict(self: Self) -> Dict:
        ...

    # Model methods
    @classmethod
    def find(cls, id: int) -> Self:
        ...

    @classmethod
    def all(cls) -> List[Self]:
        ...

    def store(self: Self) -> None:
        ...

    def save(self: Self) -> None:
        ...
