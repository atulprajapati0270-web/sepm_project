from flask import Blueprint, render_template, request
from ..models import ShahiSnan

shahi_snan_bp = Blueprint("shahi_snan", __name__, url_prefix="/shahi-snan")

@shahi_snan_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = ShahiSnan.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [ShahiSnan.route_name],
            "accommodation": [ShahiSnan.name, ShahiSnan.type, ShahiSnan.location],
            "food": [ShahiSnan.name, ShahiSnan.category, ShahiSnan.location],
            "medical": [ShahiSnan.name, ShahiSnan.type, ShahiSnan.location],
            "events": [ShahiSnan.name, ShahiSnan.location, ShahiSnan.description],
            "shahi_snan": [ShahiSnan.location, ShahiSnan.instructions],
            "security": [ShahiSnan.title, ShahiSnan.safety_information],
            "temples": [ShahiSnan.name, ShahiSnan.location, ShahiSnan.description],
            "emergency": [ShahiSnan.category, ShahiSnan.number, ShahiSnan.details],
            "notifications": [ShahiSnan.title, ShahiSnan.message, ShahiSnan.priority],
        }["shahi_snan"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(ShahiSnan, "date").desc() if "shahi_snan" in ["events","shahi_snan","notifications"] else getattr(ShahiSnan, "date")).all()
    return render_template("shahi_snan/shahi_snan.html", items=items, title="Shahi Snan Information", q=q)
