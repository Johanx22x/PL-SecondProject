from flask import Blueprint

bp = Blueprint("bills", __name__, url_prefix="/bill")

from app.bills import routes

__all__ = ["routes"]
