from flask import Blueprint, render_template, request
from ..extensions import or_
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
@traffic_bp.route("/api")
def traffic_api():
    items = Route.query.order_by(Route.route_name).all()

    return {
        "routes": [
            {
                "route_name": item.route_name,
                "status": item.status,
                "restriction": item.restriction,
                "parking": item.parking,
                "alternate_route": item.alternate_route,
                "details": item.details
            }
            for item in items
        ]
    }