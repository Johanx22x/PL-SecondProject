from typing import Protocol, List, Any, Dict


class Modelable(Protocol):
    @staticmethod
    def from_row(row: List[Any]):
        ...

    @staticmethod
    def from_rows(rows: List[List[Any]]) -> List:
        ...

    @staticmethod
    def from_form(form: Dict):
        ...

    def to_dict(self) -> Dict:
        ...
