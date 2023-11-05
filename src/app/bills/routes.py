from app.bills import bp
from app.models.bill import Bill, BillForm
from app.models.bill import Bill, BillForm
from typing import cast

from flask import abort, request



@bp.get("/")
def all():
    return [bill.to_dict() for bill in Bill.all()]


@bp.get("/<id>")
def find(id: int):
    bill = Bill.find(id)
    if bill is None:
        abort(404)
    return bill.to_dict()


@bp.get("/<id>/orders")
def get_orders(id: int):
    bill = Bill.find(id)
    if bill is None:
        abort(404)
    orders = bill.orders
    if orders is None:
        abort(404)
    return list(map(lambda order: order.to_dict(), orders))


@bp.post("/")
def create():
    casted_bill_form: BillForm = cast(BillForm, request.json)
    new_bill = Bill.from_form(casted_bill_form)
    try:
        new_bill.store()
    except Exception:
        abort(500)
    return new_bill.to_dict()


@bp.put("/<id>")
def update(id: int):
    casted_bill_form: BillForm = cast(BillForm, request.json)
    to_update = Bill.from_form(casted_bill_form).with_id(id)
    try:
        to_update.save()
    except Exception:
        abort(500)
    return to_update.to_dict()


@bp.put("/<id>/pay")
def pay(id: int):
    bill = Bill.find(id)
    if bill is None:
        abort(404)
    try:
        bill.pay()
    except Exception:
        abort(500)
    return bill.to_dict()


@bp.delete("/<id>")
def delete(id: int):
    bill = Bill.find(id)
    if bill is None:
        abort(404)
    try:
        bill.delete()
    except Exception:
        abort(500)
    return bill.to_dict()
