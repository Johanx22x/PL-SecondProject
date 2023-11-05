from typing import cast

from flask import abort, request

from app.models.table import Table, TableForm
from app.tables import bp


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
    casted_table_form: TableForm = cast(TableForm, request.json)
    new_table = Table.from_form(casted_table_form)
    try:
        new_table.store()
    except Exception:
        abort(500)
    return new_table.to_dict()


@bp.post("/<id>/update")
def update():
    casted_table_form: TableForm = cast(TableForm, request.json)
    to_update = Table.from_form(casted_table_form)
    try:
        to_update.save()
    except Exception:
        abort(500)
    return to_update.to_dict()

@bp.delete("/<id>")
def delete(id: int):
    table = Table.find(id)
    if table is None:
        abort(404)
    try:
        table.delete()
    except Exception:
        abort(501)
    return table.to_dict()
