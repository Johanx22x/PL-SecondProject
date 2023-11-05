from app.orders import bp
from typing import cast

from flask import abort, request

from app.models.order import Order, OrderForm


@bp.get("/")
def all():
    return [order.to_dict() for order in Order.all()]


@bp.get("/<id>")
def find(id: int):
    order = Order.find(id)
    if order is None:
        abort(404)
    return order.to_dict()


@bp.post("/")
def create():
    casted_order_form: OrderForm = cast(OrderForm, request.json)
    new_order = Order.from_form(casted_order_form)
    try:
        new_order.store()
    except Exception:
        abort(500)

    return new_order.to_dict()


@bp.post("/<id>/update")
def update(id: int):
    casted_order_form: OrderForm = cast(OrderForm, request.json)
    to_update = Order.from_form(casted_order_form).with_id(id)
    try:
        to_update.save()
    except Exception:
        abort(500)
    return to_update.to_dict()
