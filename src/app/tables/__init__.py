from flask import Blueprint

bp = Blueprint("table", __name__, url_prefix="/table")

from app.tables import routes

__all__ = ["routes"]
