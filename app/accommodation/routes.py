from flask import Blueprint, render_template, request
from ..models import Accommodation

accommodation_bp = Blueprint("accommodation", __name__, url_prefix="/accommodation")

@accommodation_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = Accommodation.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [Accommodation.route_name],
            "accommodation": [Accommodation.name, Accommodation.type, Accommodation.location],
            "food": [Accommodation.name, Accommodation.category, Accommodation.location],
            "medical": [Accommodation.name, Accommodation.type, Accommodation.location],
            "events": [Accommodation.name, Accommodation.location, Accommodation.description],
            "shahi_snan": [Accommodation.location, Accommodation.instructions],
            "security": [Accommodation.title, Accommodation.safety_information],
            "temples": [Accommodation.name, Accommodation.location, Accommodation.description],
            "emergency": [Accommodation.category, Accommodation.number, Accommodation.details],
            "notifications": [Accommodation.title, Accommodation.message, Accommodation.priority],
        }["accommodation"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(Accommodation, "name").desc() if "accommodation" in ["events","shahi_snan","notifications"] else getattr(Accommodation, "name")).all()
    return render_template("accommodation/accommodation.html", items=items, title="Accommodation", q=q)
