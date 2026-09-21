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
        search_fields = [Notification.title, Notification.message, Notification.priority]
        from ..extensions import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(Notification, "date").desc() if "notifications" in ["events","shahi_snan","notifications"] else getattr(Notification, "date")).all()
    return render_template("notifications/notifications.html", items=items, title="Notifications and Alerts", q=q)
