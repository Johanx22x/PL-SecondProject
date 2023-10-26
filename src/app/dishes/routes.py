from flask import abort, request
from typing import cast
from app.dishes import bp
from app.models.dish import Dish, DishForm


@bp.get("/")
def all():
    return [dish.to_dict() for dish in Dish.all()]


@bp.get("/<id>")
def find(id: int):
    dish = Dish.find(id)
    if dish is None:
        abort(404)
    return dish.to_dict()


@bp.post("/")
def create():
    casted_dish_form: DishForm = cast(DishForm, request.form)
    new_dish = Dish.from_form(casted_dish_form)
    try:
        new_dish.store()
    except Exception:
        abort(501)
    return new_dish.to_dict()


@bp.post("/<id>/update")
def update(id: int):
    casted_dish_form: DishForm = cast(DishForm, request.form)
    to_update = Dish.from_form(casted_dish_form).with_id(id)
    try:
        to_update.save()
    except Exception:
        abort(501)
    return to_update.to_dict()
