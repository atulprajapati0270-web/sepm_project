from flask import Blueprint, render_template, request
from ..models import SecurityInfo

security_bp = Blueprint("security", __name__, url_prefix="/security")

@security_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = SecurityInfo.query
    if q:
        search_fields = [SecurityInfo.title, SecurityInfo.police_help_point, SecurityInfo.safety_information, SecurityInfo.alert_level]
        from ..extensions import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(SecurityInfo, "title").desc() if "security" in ["events","shahi_snan","notifications"] else getattr(SecurityInfo, "title")).all()
    return render_template("security/security.html", items=items, title="Security and Safety", q=q)
