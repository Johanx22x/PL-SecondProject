from app.statistics import bp
from flask import abort, request

from app.models.statistic import Statistic


@bp.route("/", methods=["GET"])
def all():
    return [statistic.to_dict() for statistic in Statistic.all()]


@bp.route("/<int:id>", methods=["GET"])
def find(id: int):
    statistic = Statistic.find(id)
    if statistic is None:
        abort(404)
    return statistic.to_dict()


@bp.route("/latest", methods=["GET"])
def latest():
    statistic = Statistic.latest()
    if statistic is None:
        abort(404)
    return statistic.to_dict()


@bp.route("/date-range", methods=["GET"])
def sales_and_income_by_date_range():
    args = request.args
    start = args.get("start")
    end = args.get("end")
    statistics = Statistic.sales_and_income_by_date_range(start, end)
    if statistics is None:
        abort(404)
    # This has the format [["2020-01-01", 1, 1.0], ...]
    return statistics


@bp.route("/top-menu-items", methods=["GET"])
def top_menu_items():
    statistics = Statistic.top_menu_items()
    if statistics is None:
        abort(404)
    return statistics


@bp.route("/top-inventory-items", methods=["GET"])
def top_inventory_items():
    statistics = Statistic.top_inventory_items()
    if statistics is None:
        abort(404)
    return statistics
