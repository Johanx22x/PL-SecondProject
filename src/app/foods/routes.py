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
    casted_food_form: FoodForm = cast(FoodForm, request.form)
    new_food = Food.from_form(casted_food_form)
    try:
        new_food.store()
    except Exception:
        abort(501)
    return new_food.to_dict()


@bp.post("/<id>/update")
def update(id: int):
    casted_food_form: FoodForm = cast(FoodForm, request.form)
    to_update = Food.from_form(casted_food_form).with_id(id)
    try:
        to_update.save()
    except Exception:
        abort(501)
    return to_update.to_dict()

# Delete food 
@bp.delete("/<id>/delete")
def delete(id: int):
    food = Food.find(id)
    if food is None:
        abort(404)
    try:
        food.delete()
    except Exception:
        return abort(501)
    return food.to_dict()
