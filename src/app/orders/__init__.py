from flask import Blueprint

bp = Blueprint("order", __name__, url_prefix="/order")

from app.orders import routes

__all__ = ["routes"]
