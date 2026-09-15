from flask import Blueprint, render_template, request
from ..models import Route

traffic_bp = Blueprint("traffic", __name__, url_prefix="/traffic")

@traffic_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = Route.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [Route.route_name],
            "accommodation": [Route.name, Route.type, Route.location],
            "food": [Route.name, Route.category, Route.location],
            "medical": [Route.name, Route.type, Route.location],
            "events": [Route.name, Route.location, Route.description],
            "shahi_snan": [Route.location, Route.instructions],
            "security": [Route.title, Route.safety_information],
            "temples": [Route.name, Route.location, Route.description],
            "emergency": [Route.category, Route.number, Route.details],
            "notifications": [Route.title, Route.message, Route.priority],
        }["traffic"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(Route, "route_name").desc() if "traffic" in ["events","shahi_snan","notifications"] else getattr(Route, "route_name")).all()
    return render_template("traffic/traffic.html", items=items, title="Traffic and Routes", q=q)
