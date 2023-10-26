from typing import Self
from flask import Flask


class Program:
    def __init__(self: Self, server_name: str = __name__) -> None:
        self._server = Flask(server_name)

    def run(self):
        """Main entry point of the program."""
        self._serve()

    def _serve(self: Self) -> None:
        from app.bills import bp as bill_routes
        from app.dishes import bp as dish_routes
        from app.foods import bp as food_routes
        from app.orders import bp as order_routes
        from app.tables import bp as table_routes

        self._server.register_blueprint(bill_routes)
        self._server.register_blueprint(dish_routes)
        self._server.register_blueprint(food_routes)
        self._server.register_blueprint(order_routes)
        self._server.register_blueprint(table_routes)
        self._server.run(debug=True)
