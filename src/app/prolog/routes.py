from app.prolog import bp
from flask import abort, request
from app.prolog import Prolog

@bp.post("/<string:query>")
def query(query: str):
    if query is None:
        abort(400)
    prolog = Prolog()
    try:
        result = prolog.query(query)
        return result
    except Exception as e:
        abort(400, str(e))
