from typing import cast

from flask import abort, request

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
    casted_dish_form: DishForm = cast(DishForm, request.json)
    new_dish = Dish.from_form(casted_dish_form)
    try:
        new_dish.store()
    except Exception:
        abort(500)
    return new_dish.to_dict()


@bp.post("/<id>")
def update(id: int):
    casted_dish_form: DishForm = cast(DishForm, request.json)
    to_update = Dish.from_form(casted_dish_form).with_id(id)
    try:
        to_update.save()
    except Exception:
        abort(500)
    return to_update.to_dict()

@bp.delete("/<id>")
def delete(id: int):
    dish = Dish.find(id)
    if dish is None:
        abort(404)
    try:
        dish.delete()
    except Exception:
        return abort(500)
    return dish.to_dict()
