from flask import Blueprint, render_template, request
from ..models import EmergencyHelpline

emergency_bp = Blueprint("emergency", __name__, url_prefix="/emergency")

@emergency_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = EmergencyHelpline.query
    if q:
        search_fields = [EmergencyHelpline.category, EmergencyHelpline.number, EmergencyHelpline.details]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(EmergencyHelpline, "category").desc() if "emergency" in ["events","shahi_snan","notifications"] else getattr(EmergencyHelpline, "category")).all()
    return render_template("emergency/emergency.html", items=items, title="Emergency Helpline", q=q)
