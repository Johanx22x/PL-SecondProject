from flask import Blueprint

from app.orders import routes

bp = Blueprint("order", __name__, url_prefix="/order")



__all__ = ["routes"]
