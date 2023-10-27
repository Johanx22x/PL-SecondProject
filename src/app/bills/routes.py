from typing import cast
from flask import abort, request
from app.models.bill import Bill, BillForm
from app.bills import bp


@bp.get("/")
def all():
    return [bill.to_dict() for bill in Bill.all()]


@bp.get("/<id>")
def find(id: int):
    bill = Bill.find(id)
    if bill is None:
        abort(404)
    return bill.to_dict()


@bp.post("/")
def create():
    casted_bill_form: BillForm = cast(BillForm, request.form)
    new_bill = Bill.from_form(casted_bill_form)
    try:
        new_bill.store()
    except Exception:
        abort(501)
    return new_bill.to_dict()


@bp.post("/<id>/update")
def update(id: int):
    casted_bill_form: BillForm = cast(BillForm, request.form)
    to_update = Bill.from_form(casted_bill_form).with_id(id)
    try:
        to_update.save()
    except Exception:
        abort(501)
    return to_update.to_dict()