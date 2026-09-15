from flask import Blueprint, render_template, request
from ..models import SecurityInfo

security_bp = Blueprint("security", __name__, url_prefix="/security")

@security_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = SecurityInfo.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [SecurityInfo.route_name],
            "accommodation": [SecurityInfo.name, SecurityInfo.type, SecurityInfo.location],
            "food": [SecurityInfo.name, SecurityInfo.category, SecurityInfo.location],
            "medical": [SecurityInfo.name, SecurityInfo.type, SecurityInfo.location],
            "events": [SecurityInfo.name, SecurityInfo.location, SecurityInfo.description],
            "shahi_snan": [SecurityInfo.location, SecurityInfo.instructions],
            "security": [SecurityInfo.title, SecurityInfo.safety_information],
            "temples": [SecurityInfo.name, SecurityInfo.location, SecurityInfo.description],
            "emergency": [SecurityInfo.category, SecurityInfo.number, SecurityInfo.details],
            "notifications": [SecurityInfo.title, SecurityInfo.message, SecurityInfo.priority],
        }["security"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(SecurityInfo, "title").desc() if "security" in ["events","shahi_snan","notifications"] else getattr(SecurityInfo, "title")).all()
    return render_template("security/security.html", items=items, title="Security and Safety", q=q)
