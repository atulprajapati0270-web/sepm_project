from flask import Blueprint, render_template, request
from sqlalchemy import or_
from ..models import Route

traffic_bp = Blueprint("traffic", __name__, url_prefix="/traffic")


@traffic_bp.route("/")
def index():
    q = request.args.get("q", "").strip()

    query = Route.query

    if q:
        query = query.filter(
            or_(
                Route.route_name.ilike(f"%{q}%"),
                Route.status.ilike(f"%{q}%"),
                Route.restriction.ilike(f"%{q}%"),
                Route.parking.ilike(f"%{q}%"),
                Route.alternate_route.ilike(f"%{q}%"),
                Route.details.ilike(f"%{q}%")
            )
        )

    items = query.order_by(Route.route_name).all()

    return render_template(
        "traffic/traffic.html",
        items=items,
        title="Traffic and Routes",
        q=q
    )