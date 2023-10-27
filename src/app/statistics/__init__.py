from flask import Blueprint

bp = Blueprint("statistics", __name__, url_prefix="/statistic")

from app.statistics import routes

__all__ = ["routes"]
