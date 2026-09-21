from flask import Blueprint, render_template, request
from ..models import Event

events_bp = Blueprint("events", __name__, url_prefix="/events")

@events_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = Event.query
    if q:
        search_fields = [Event.name, Event.location, Event.description]
        from ..extensions import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(Event.date.asc(), Event.time.asc(), Event.name.asc()).all()
    return render_template(
        "events/events.html",
        items=items,
        next_event=items[0] if items else None,
        title="Events and Programmes",
        q=q,
    )
