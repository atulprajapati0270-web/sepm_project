from flask import Blueprint, render_template, request
from ..models import Event

events_bp = Blueprint("events", __name__, url_prefix="/events")

@events_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = Event.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [Event.route_name],
            "accommodation": [Event.name, Event.type, Event.location],
            "food": [Event.name, Event.category, Event.location],
            "medical": [Event.name, Event.type, Event.location],
            "events": [Event.name, Event.location, Event.description],
            "shahi_snan": [Event.location, Event.instructions],
            "security": [Event.title, Event.safety_information],
            "temples": [Event.name, Event.location, Event.description],
            "emergency": [Event.category, Event.number, Event.details],
            "notifications": [Event.title, Event.message, Event.priority],
        }["events"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(Event, "name").desc() if "events" in ["events","shahi_snan","notifications"] else getattr(Event, "name")).all()
    return render_template("events/events.html", items=items, title="Events and Programmes", q=q)
