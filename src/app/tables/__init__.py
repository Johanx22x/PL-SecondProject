from flask import Blueprint

from app.tables import routes

bp = Blueprint("table", __name__, url_prefix="/table")


__all__ = ["routes"]
