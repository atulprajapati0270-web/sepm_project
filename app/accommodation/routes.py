from flask import Blueprint, render_template, request
from ..models import Accommodation

accommodation_bp = Blueprint("accommodation", __name__, url_prefix="/accommodation")

@accommodation_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = Accommodation.query
    if q:
        search_fields = [Accommodation.name, Accommodation.type, Accommodation.location, Accommodation.details]
        from ..extensions import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(Accommodation, "name").desc() if "accommodation" in ["events","shahi_snan","notifications"] else getattr(Accommodation, "name")).all()
    return render_template("accommodation/accommodation.html", items=items, title="Accommodation", q=q)
