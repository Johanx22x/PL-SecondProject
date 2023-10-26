from typing import cast
from flask import abort, request
from app.tables import bp
from app.models.table import Table, TableForm


@bp.get("/")
def all():
    return [table.to_dict() for table in Table.all()]


@bp.get("/<id>")
def find(id: int):
    table = Table.find(id)
    if table is None:
        abort(404)
    return table.to_dict()


@bp.post("/")
def create():
    casted_table_form: TableForm = cast(TableForm, request.form)
    new_table = Table.from_form(casted_table_form)
    try:
        new_table.store()
    except Exception:
        abort(501)
    return new_table.to_dict()


@bp.post("/<id>/update")
def update():
    casted_table_form: TableForm = cast(TableForm, request.form)
    to_update = Table.from_form(casted_table_form)
    try:
        to_update.save()
    except Exception:
        abort(501)
    return to_update.to_dict()
