from flask import Blueprint

from app.dishes import routes

bp = Blueprint("dish", __name__, url_prefix="/dish")


__all__ = ["routes"]
