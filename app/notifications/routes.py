from flask import Blueprint, render_template, request
from ..integrations.google_updates import sync_google_updates
from ..models import Notification

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

@notifications_bp.route("/")
def index():
    sync_google_updates()
    q = request.args.get("q", "").strip()
    query = Notification.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [Notification.route_name],
            "accommodation": [Notification.name, Notification.type, Notification.location],
            "food": [Notification.name, Notification.category, Notification.location],
            "medical": [Notification.name, Notification.type, Notification.location],
            "events": [Notification.name, Notification.location, Notification.description],
            "shahi_snan": [Notification.location, Notification.instructions],
            "security": [Notification.title, Notification.safety_information],
            "temples": [Notification.name, Notification.location, Notification.description],
            "emergency": [Notification.category, Notification.number, Notification.details],
            "notifications": [Notification.title, Notification.message, Notification.priority],
        }["notifications"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(Notification, "date").desc() if "notifications" in ["events","shahi_snan","notifications"] else getattr(Notification, "date")).all()
    return render_template("notifications/notifications.html", items=items, title="Notifications and Alerts", q=q)
