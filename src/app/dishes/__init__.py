from flask import Blueprint

bp = Blueprint("dish", __name__, url_prefix="/dish")

from app.dishes import routes

__all__ = ["routes"]
