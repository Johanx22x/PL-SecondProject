from os import getcwd

from flask import Blueprint

from app.static_serve import routes

bp = Blueprint("static_serve", __name__, static_folder=f"{getcwd()}/src/app/frontend/dist")



__all__ = ["routes"]
