from typing import Self

from flask import Flask
from flask_cors import CORS


class Program:
    def __init__(
        self: Self, server_name: str = __name__, static_folder="static"
    ) -> None:
        self._server = Flask(server_name, static_folder=static_folder)

    def run(self):
        """Main entry point of the program."""
        CORS(self._server, resources={r"/*": {"origins": "*"}})
        self._register_routes()
        self._serve()

    def _register_routes(self: Self) -> None:
        from app.bills import bp as bill_routes
        from app.dishes import bp as dish_routes
        from app.foods import bp as food_routes
        from app.orders import bp as order_routes
        from app.statistics import bp as statistic_routes
        from app.tables import bp as table_routes
        from app.static_serve import bp as static_routes

        self._server.register_blueprint(bill_routes, url_prefix="/api/bill")
        self._server.register_blueprint(dish_routes, url_prefix="/api/dish")
        self._server.register_blueprint(food_routes, url_prefix="/api/food")
        self._server.register_blueprint(
            statistic_routes, url_prefix="/api/statistic"
        )
        self._server.register_blueprint(order_routes, url_prefix="/api/order")
        self._server.register_blueprint(table_routes, url_prefix="/api/table")
        self._server.register_blueprint(static_routes)

    def _serve(self: Self) -> None:
        self._server.run(debug=True)
