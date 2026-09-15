from flask import Blueprint, render_template
from ..models import Notification

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    notifications = Notification.query.order_by(Notification.date.desc()).limit(5).all()
    return render_template("home.html", notifications=notifications)

@main_bp.route("/help")
def help_page():
    return render_template("help.html")
