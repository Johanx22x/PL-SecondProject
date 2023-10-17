from flask import Blueprint

bp = Blueprint("food", __name__, url_prefix="/food")

from app.foods import routes

__all__ = ["routes"]
