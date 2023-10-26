from typing import Self, List
import sqlite3
from singleton import SingletonMeta


class SQLite(metaclass=SingletonMeta):
    """SQLite class."""

    def __init__(self: Self, db_name: str) -> None:
        """Initialize the SQLite class."""
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute(self: Self, query: str, values: list = None):
        """Execute a query."""
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.connection.commit()

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
