from os import getcwd

from flask import Blueprint

bp = Blueprint(
    "static_serve", __name__, static_folder=f"{getcwd()}/src/app/frontend/dist"
)

from app.static_serve import routes



__all__ = ["routes"]
