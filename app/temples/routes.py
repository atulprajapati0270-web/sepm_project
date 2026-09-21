from flask import Blueprint, render_template, request
from ..models import Temple

temples_bp = Blueprint("temples", __name__, url_prefix="/temples")

@temples_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = Temple.query
    if q:
        search_fields = [Temple.name, Temple.location, Temple.description]
        from ..extensions import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(Temple, "name").desc() if "temples" in ["events","shahi_snan","notifications"] else getattr(Temple, "name")).all()
    return render_template("temples/temples.html", items=items, title="Famous and Nearby Temples", q=q)
