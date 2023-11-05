from typing import cast

from flask import abort, request

from app.foods import bp
from app.models.food import Food, FoodForm


@bp.get("/")
def all():
    return [food.to_dict() for food in Food.all()]


@bp.get("/<id>")
def find(id: int):
    food = Food.find(id)
    if food is None:
        abort(404)
    return food.to_dict()


@bp.post("/")
def create():
    casted_food_form: FoodForm = cast(FoodForm, request.json)
    new_food = Food.from_form(casted_food_form)
    try:
        new_food.store()
    except Exception:
        abort(500)
    return new_food.to_dict()


@bp.post("/<id>")
def update(id: int):
    casted_food_form: FoodForm = cast(FoodForm, request.json)
    to_update = Food.from_form(casted_food_form).with_id(id)
    try:
        to_update.save()
    except Exception:
        abort(500)
    return to_update.to_dict()


# Delete food
@bp.delete("/<id>")
def delete(id: int):
    food = Food.find(id)
    if food is None:
        abort(404)
    try:
        food.delete()
    except Exception:
        return abort(500)
    return food.to_dict()
