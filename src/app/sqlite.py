from typing import Self, List, Optional
import sqlite3
from sqlite3 import Cursor
from app.singleton import SingletonMeta


class SQLite(metaclass=SingletonMeta):
    """SQLite class."""

    def __init__(self: Self, db_name: Optional[str] = "data.sqlite") -> None:
        """Initialize the SQLite class."""
        if not db_name:
            return
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.execute("PRAGMA foreign_keys=ON;")
        self.connection.execute("PRAGMA encoding='UTF-8';")

    def execute(self: Self, query: str, values: List = []) -> Cursor:
        """Execute a query."""
        return self.connection.execute(query, values)

    def close(self: Self) -> None:
        """Close the SQLite connection."""
        self.connection.close()

        del SingletonMeta._instances[self.__class__]


if __name__ == "__main__":
    # Initialize
    sqlite = SQLite("../testdb.sqlite")

    # Close
    sqlite.close()
