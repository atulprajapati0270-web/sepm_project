from flask import render_template
from . import maps_bp


@maps_bp.route("/")
def index():
    return render_template("maps/map.html")