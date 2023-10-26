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
        self.connection.execute("PRAGMA foreign_keys = on;")
        self.connection.execute("PRAGMA encoding = 'UTF-8';")
        self.cursor = self.connection.cursor()

    def execute(self: Self, query: str, values: List = []) -> Cursor:
        """Execute a query."""
        cur = self.cursor.execute(query, values)
        return cur

    def fetch_all(self: Self) -> List:
        """Fetch all results."""
        return self.cursor.fetchall()

    def close(self: Self) -> None:
        """Close the SQLite connection."""
        self.cursor.close()
        self.connection.close()

        del SingletonMeta._instances[self.__class__]


if __name__ == "__main__":
    # Initialize
    sqlite = SQLite("../testdb.sqlite")

    # Execute
    sqlite.execute("SELECT * FROM Foods")
    print(sqlite.fetch_all())

    # Close
    sqlite.close()
