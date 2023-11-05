from app.static_serve import bp

# @bp.route("/favicon.ico")
# def favicon():
#     return bp.send_static_file("favicon.ico")

# TODO: Find a better way of routing this


@bp.route("/static/js/<filename>")
def js(filename: str):
    return bp.send_static_file(f"static/js/{filename}")


@bp.route("/static/img/<filename>")
def img(filename: str):
    return bp.send_static_file(f"static/img/{filename}")


@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def static_files(_):
    return bp.send_static_file("index.html")
