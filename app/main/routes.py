from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from ..integrations.google_updates import sync_google_updates
from ..models import Notification, Temple

main_bp = Blueprint("main", __name__)

@main_bp.route("/language/<lang>")
def language(lang):
    if lang in ("hi", "en"):
        session["lang"] = lang
        session.modified = True
    next_url = request.args.get("next", "").strip()
    if next_url.endswith("?"):
        next_url = next_url[:-1]
    if next_url.startswith("/") and not next_url.startswith("//"):
        return redirect(next_url or "/")
    return redirect(request.referrer or url_for("main.home"))

@main_bp.route("/")
def home():
    sync_google_updates()
    notifications = Notification.query.order_by(Notification.date.desc()).limit(5).all()
    temples = Temple.query.order_by(Temple.name.asc()).limit(4).all()
    return render_template("home.html", notifications=notifications, temples=temples)

@main_bp.route("/help")
def help_page():
    return render_template("help.html")


@main_bp.route("/assistant", methods=["POST"])
def assistant():
    question = request.get_json(silent=True) or {}
    message = str(question.get("message", "")).strip().lower()
    location = question.get("location") or {}
    has_location = isinstance(location, dict) and isinstance(location.get("latitude"), (int, float)) and isinstance(location.get("longitude"), (int, float))

    if any(word in message for word in ("hello", "hi", "namaste", "start")):
        answer = "Namaste. I can help you plan Ujjain: places to visit, nearby cities, food, stay, routes, events, Shahi Snan, and emergency help."
        links = [("Explore Ujjain temples", "/temples/"), ("See the city map", "/maps/")]
    elif any(word in message for word in ("near", "city", "indore", "dewas", "omkareshwar", "bhopal", "mandu")):
        answer = "Useful nearby destinations from Ujjain are Dewas (about 40 km), Indore (about 55 km), Omkareshwar (about 140 km), Mandu (about 150 km), and Bhopal (about 190 km). Travel times vary with traffic and Simhastha restrictions, so check routes before leaving."
        links = [("Check traffic and routes", "/traffic/"), ("Open the city map", "/maps/")]
    elif any(word in message for word in ("food", "eat", "hotel", "restaurant", "bhojan", "stall")):
        answer = "For food, start with the Ujjain food guide. It includes hotels, food stalls, bhojanalayas, and facilities around Mahakal, Ram Ghat, Freeganj, Nanakheda, and transit areas. Confirm timings and availability locally."
        links = [("Find food nearby", "/food/"), ("Find a place to stay", "/accommodation/")]
    elif any(word in message for word in ("temple", "mahakal", "darshan", "visit", "place")):
        answer = "Begin with Mahakaleshwar and the nearby temple circuit, then plan time for Ram Ghat and the Shipra riverfront. Keep your entry documents and follow the latest official crowd and darshan instructions."
        links = [("Temple guide", "/temples/"), ("Latest alerts", "/notifications/")]
    elif any(word in message for word in ("event", "programme", "program", "simhastha")):
        answer = "The Events page contains the administrator-published Simhastha programme. Dates, venues, and timings can change, so check it again before travelling."
        links = [("View Simhastha events", "/events/"), ("Read alerts", "/notifications/")]
    elif any(word in message for word in ("snan", "bath", "shahi")):
        answer = "The Shahi Snan page shows the currently published bathing schedule and verification status. Use only verified official information when planning your visit."
        links = [("Shahi Snan updates", "/shahi-snan/"), ("Check routes", "/traffic/")]
    elif any(word in message for word in ("emergency", "help", "medical", "police", "ambulance", "lost")):
        answer = "For an immediate emergency, contact local emergency services first. This app also provides emergency contacts, medical facilities, and Lost & Found support."
        links = [("Emergency contacts", "/emergency/"), ("Medical help", "/medical/")]
    elif any(word in message for word in ("route", "transport", "bus", "train", "travel", "airport")):
        answer = "Use the map and traffic pages to plan movement around Ujjain. Indore is the nearest major airport city, while Ujjain has rail and road connections; allow extra time during major bathing days."
        links = [("Traffic and routes", "/traffic/"), ("Open the map", "/maps/")]
    else:
        answer = "I can guide you around Ujjain and Simhastha. Try asking: 'What cities are near Ujjain?', 'Where can I find food?', 'What should I visit?', or 'Show Shahi Snan updates.'"
        links = [("Start with the visitor guide", "/help/"), ("See all services", "/")]

    if has_location and any(word in message for word in ("near", "nearby", "closest", "around", "food", "medical", "hospital", "emergency", "hotel", "stay")):
        answer += " I can use your current map location for nearby results; your coordinates are used for this request only and are not saved."

    return jsonify({"answer": answer, "links": [{"label": label, "url": url} for label, url in links], "location_used": has_location})
