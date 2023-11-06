from flask import Blueprint
from typing import Any, List, Self
from swiplserver import PrologMQI
from app.singleton import SingletonMeta


class Prolog(metaclass=SingletonMeta):
    """Prolog class."""

    def __init__(self: Self) -> None:
        """Initialize the Prolog class."""
        self.mqi = PrologMQI()
        self.prolog_thread = self.mqi.create_thread()

        # Set encoding
        self.prolog_thread.query("set_prolog_flag(encoding,utf8).")

    def query(self: Self, query_str: str) -> List[Any] | Any | bool | None:
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


bp = Blueprint("prolog", __name__, url_prefix="/prolog")

from app.prolog import routes

__all__ = ["routes"]
