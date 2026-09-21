from flask import Blueprint, render_template, request
from ..models import ShahiSnan

shahi_snan_bp = Blueprint("shahi_snan", __name__, url_prefix="/shahi-snan")

@shahi_snan_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = ShahiSnan.query
    if q:
        search_fields = [ShahiSnan.location, ShahiSnan.instructions, ShahiSnan.verification_note]
        from ..extensions import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(ShahiSnan.date.asc(), ShahiSnan.time.asc()).all()
    return render_template(
        "shahi_snan/shahi_snan.html",
        items=items,
        next_snan=items[0] if items else None,
        title="Shahi Snan Information",
        q=q,
    )
