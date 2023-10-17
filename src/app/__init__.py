from typing import Self
from flask import Flask
from app.extensions import db


class Program:
    def __init__(self: Self, server_name: str = __name__) -> None:
        self._server = Flask(server_name)

    def run(self):
        """Main entry point of the program."""
        self._serve()
        db.close()

    def _serve(self: Self) -> None:
        from app.foods import bp as food_routes
        from app.dishes import bp as dish_routes

        self._server.register_blueprint(food_routes)
        self._server.register_blueprint(dish_routes)
        self._server.run(debug=True)
