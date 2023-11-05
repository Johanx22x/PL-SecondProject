from flask import Blueprint

from app.foods import routes

bp = Blueprint("food", __name__, url_prefix="/food")


__all__ = ["routes"]
