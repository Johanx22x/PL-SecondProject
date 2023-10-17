from flask import abort, request
from typing import cast
from app.dishes import bp
from app.extensions import db
from app.models.dish import Dish, DishForm


@bp.get("/")
def all_dishes():
    c = db.execute("SELECT * FROM Dishes")
    rows = Dish.from_rows(c.fetchall())
    c.close()
    db.commit()
    return [row.to_dict() for row in rows]


@bp.get("/<id>")
def dish(id: int):
    c = db.execute("SELECT * FROM Dishes WHERE id = ?", [id])
    items = c.fetchall()
    if len(items) == 0:
        abort(404)
    c.close()
    db.commit()
    return Dish.from_row(items[0]).to_dict()

@bp.post("/")
def create_dish():
    casted_dish_form: DishForm = cast(DishForm, request.form)
    new_dish = Dish.from_form(casted_dish_form)

    c = db.execute(
        "INSERT INTO Dishes (name, type) VALUES (?, ?)",
        new_dish.values,
    )
    if c.lastrowid:
        new_dish.with_id(c.lastrowid)

    c.close()
    db.commit()

    return new_dish.to_dict()
