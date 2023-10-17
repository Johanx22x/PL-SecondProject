from typing import cast
from flask import abort, jsonify, request
from app.foods import bp
from app.models.food import Food, FoodForm
from app.extensions import db


@bp.get("/")
def all_food():
    c = db.execute("SELECT * from Foods")
    res = Food.from_rows(c.fetchall())
    return [food.to_dict() for food in res]


@bp.get("/<id>")
def food(id: int):
    c = db.execute("SELECT * FROM Foods WHERE id = ?", [id])
    items = c.fetchall()
    if len(items) == 0:
        abort(404)
    c.close()
    db.commit()
    return Food.from_row(items[0]).to_dict()


@bp.post("/")
def create_food():
    casted_food_form: FoodForm = cast(FoodForm, request.form)
    new_food = Food.from_form(casted_food_form)

    c = db.execute(
        "INSERT INTO Foods (type, subtype, name, calories, price) VALUES (?, ?, ?, ?, ?)",
        new_food.values,
    )
    if c.lastrowid:
        new_food.with_id(c.lastrowid)

    c.close()
    db.commit()

    return new_food.to_dict()
