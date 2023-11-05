from flask import Blueprint

from app.statistics import routes

bp = Blueprint("statistics", __name__, url_prefix="/statistic")



__all__ = ["routes"]
