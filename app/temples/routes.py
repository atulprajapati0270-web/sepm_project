from flask import Blueprint, render_template, request
from ..models import Temple

temples_bp = Blueprint("temples", __name__, url_prefix="/temples")

@temples_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = Temple.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [Temple.route_name],
            "accommodation": [Temple.name, Temple.type, Temple.location],
            "food": [Temple.name, Temple.category, Temple.location],
            "medical": [Temple.name, Temple.type, Temple.location],
            "events": [Temple.name, Temple.location, Temple.description],
            "shahi_snan": [Temple.location, Temple.instructions],
            "security": [Temple.title, Temple.safety_information],
            "temples": [Temple.name, Temple.location, Temple.description],
            "emergency": [Temple.category, Temple.number, Temple.details],
            "notifications": [Temple.title, Temple.message, Temple.priority],
        }["temples"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(Temple, "name").desc() if "temples" in ["events","shahi_snan","notifications"] else getattr(Temple, "name")).all()
    return render_template("temples/temples.html", items=items, title="Famous and Nearby Temples", q=q)
