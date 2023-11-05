from flask import Blueprint

from app.bills import routes

bp = Blueprint("bills", __name__, url_prefix="/bill")



__all__ = ["routes"]
