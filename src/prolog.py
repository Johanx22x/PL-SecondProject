from typing import Self
from swiplserver import PrologMQI, PrologThread
from singleton import SingletonMeta


class Prolog(metaclass=SingletonMeta):
    """Prolog class."""

    def __init__(self: Self) -> None:
        """Initialize the Prolog class."""
        self.mqi = PrologMQI()
        self.prolog_thread = self.mqi.create_thread()

        # Set encoding
        self.prolog_thread.query("set_prolog_flag(encoding,utf8).")

    def query(self: Self, query_str: str):
        """Query the Prolog knowledge base."""
        result = self.prolog_thread.query(query_str)
        return result

    def reset(self: Self) -> None:
        """Reset the Prolog knowledge base."""
        # Close the existing PrologThread to reset the knowledge
        self.prolog_thread.stop()
        self.mqi.stop()

        # Create a new PrologThread
        self.mqi = PrologMQI()
        self.prolog_thread = self.mqi.create_thread()

    def close(self: Self) -> None:
        """Close the Prolog connection."""
        # Close the PrologThread and release resources
        self.prolog_thread.stop()
        self.mqi.stop()

        del SingletonMeta._instances[self.__class__]


if __name__ == "__main__":
    # Initialize
    prolog = Prolog()

    # Consult
    result = prolog.query("consult('./main.pl')")
    print(result)

    # Query
    result = prolog.query("parent(X, Y).")
    print(result)

    # Singleton test
    prolog = Prolog()
    result = prolog.query("parent(X, Y).")
    print(result)

    # Close or reset deletes the knowledge base
    prolog.reset()
    prolog.close()

    # When close() is called, the singleton instance is deleted
    prolog2 = Prolog()
    print(prolog is prolog2)
    prolog2.close()
