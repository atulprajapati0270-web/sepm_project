from flask import Blueprint, render_template, request
from ..models import EmergencyHelpline

emergency_bp = Blueprint("emergency", __name__, url_prefix="/emergency")

@emergency_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = EmergencyHelpline.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [EmergencyHelpline.route_name],
            "accommodation": [EmergencyHelpline.name, EmergencyHelpline.type, EmergencyHelpline.location],
            "food": [EmergencyHelpline.name, EmergencyHelpline.category, EmergencyHelpline.location],
            "medical": [EmergencyHelpline.name, EmergencyHelpline.type, EmergencyHelpline.location],
            "events": [EmergencyHelpline.name, EmergencyHelpline.location, EmergencyHelpline.description],
            "shahi_snan": [EmergencyHelpline.location, EmergencyHelpline.instructions],
            "security": [EmergencyHelpline.title, EmergencyHelpline.safety_information],
            "temples": [EmergencyHelpline.name, EmergencyHelpline.location, EmergencyHelpline.description],
            "emergency": [EmergencyHelpline.category, EmergencyHelpline.number, EmergencyHelpline.details],
            "notifications": [EmergencyHelpline.title, EmergencyHelpline.message, EmergencyHelpline.priority],
        }["emergency"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(EmergencyHelpline, "category").desc() if "emergency" in ["events","shahi_snan","notifications"] else getattr(EmergencyHelpline, "category")).all()
    return render_template("emergency/emergency.html", items=items, title="Emergency Helpline", q=q)
