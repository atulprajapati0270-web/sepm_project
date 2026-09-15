from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import (
    User, Route, Accommodation, FoodFacility, MedicalFacility, Event,
    ShahiSnan, SecurityInfo, Temple, EmergencyHelpline, Complaint,
    LostFound, Notification, AdminLog
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.role != "admin":
            flash("Administrator access required.", "danger")
            return redirect(url_for("main.home"))
        return view(*args, **kwargs)
    return wrapped

MODEL_MAP = {
    "routes": Route,
    "accommodations": Accommodation,
    "food": FoodFacility,
    "medical": MedicalFacility,
    "events": Event,
    "shahi-snan": ShahiSnan,
    "security": SecurityInfo,
    "temples": Temple,
    "emergency": EmergencyHelpline,
    "notifications": Notification,
}

@admin_bp.route("/")
@admin_required
def dashboard():
    counts = {
        "Users": User.query.count(),
        "Routes": Route.query.count(),
        "Accommodation": Accommodation.query.count(),
        "Food": FoodFacility.query.count(),
        "Medical": MedicalFacility.query.count(),
        "Events": Event.query.count(),
        "Complaints": Complaint.query.count(),
        "Lost & Found": LostFound.query.count(),
        "Notifications": Notification.query.count(),
    }
    recent_complaints = Complaint.query.order_by(Complaint.created_at.desc()).limit(8).all()
    recent_reports = LostFound.query.order_by(LostFound.created_at.desc()).limit(8).all()
    return render_template("admin/dashboard.html", counts=counts,
                           recent_complaints=recent_complaints,
                           recent_reports=recent_reports)

@admin_bp.route("/<resource>/")
@admin_required
def list_resource(resource):
    model = MODEL_MAP.get(resource)
    if not model:
        flash("Unknown admin module.", "danger")
        return redirect(url_for("admin.dashboard"))
    items = model.query.all()
    return render_template("admin/list.html", resource=resource, model=model, items=items)

@admin_bp.route("/<resource>/new", methods=["GET", "POST"])
@admin_required
def new_resource(resource):
    model = MODEL_MAP.get(resource)
    if not model:
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        obj = build_object(model, request.form)
        db.session.add(obj)
        db.session.flush()
        db.session.add(AdminLog(admin_id=current_user.id, action=f"Created {resource} #{obj.id}"))
        db.session.commit()
        flash("Record created.", "success")
        return redirect(url_for("admin.list_resource", resource=resource))
    return render_template("admin/form.html", resource=resource, model=model, item=None)

@admin_bp.route("/<resource>/<int:item_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_resource(resource, item_id):
    model = MODEL_MAP.get(resource)
    if not model:
        return redirect(url_for("admin.dashboard"))
    item = db.session.get(model, item_id)
    if not item:
        flash("Record not found.", "danger")
        return redirect(url_for("admin.list_resource", resource=resource))
    if request.method == "POST":
        build_object(model, request.form, existing=item)
        db.session.add(AdminLog(admin_id=current_user.id, action=f"Updated {resource} #{item.id}"))
        db.session.commit()
        flash("Record updated.", "success")
        return redirect(url_for("admin.list_resource", resource=resource))
    return render_template("admin/form.html", resource=resource, model=model, item=item)

@admin_bp.route("/<resource>/<int:item_id>/delete", methods=["POST"])
@admin_required
def delete_resource(resource, item_id):
    model = MODEL_MAP.get(resource)
    if not model:
        return redirect(url_for("admin.dashboard"))
    item = db.session.get(model, item_id)
    if item:
        db.session.delete(item)
        db.session.add(AdminLog(admin_id=current_user.id, action=f"Deleted {resource} #{item.id}"))
        db.session.commit()
        flash("Record deleted.", "success")
    return redirect(url_for("admin.list_resource", resource=resource))

@admin_bp.route("/complaints/")
@admin_required
def complaints():
    items = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template("admin/complaints.html", items=items)

@admin_bp.route("/complaints/<int:item_id>/status", methods=["POST"])
@admin_required
def complaint_status(item_id):
    item = db.session.get(Complaint, item_id)
    if item:
        item.status = request.form.get("status", "Submitted")
        db.session.add(AdminLog(admin_id=current_user.id, action=f"Updated complaint #{item.id} status to {item.status}"))
        db.session.commit()
        flash("Complaint status updated.", "success")
    return redirect(url_for("admin.complaints"))

@admin_bp.route("/lost-found/")
@admin_required
def lost_found():
    items = LostFound.query.order_by(LostFound.created_at.desc()).all()
    return render_template("admin/lost_found.html", items=items)

@admin_bp.route("/lost-found/<int:item_id>/status", methods=["POST"])
@admin_required
def lost_found_status(item_id):
    item = db.session.get(LostFound, item_id)
    if item:
        item.status = request.form.get("status", "Reported")
        db.session.add(AdminLog(admin_id=current_user.id, action=f"Updated Lost & Found #{item.id} status to {item.status}"))
        db.session.commit()
        flash("Lost & Found status updated.", "success")
    return redirect(url_for("admin.lost_found"))

def parse_value(column, value):
    from datetime import date, datetime, time
    if value is None:
        return None
    if isinstance(column.type, db.Date):
        return date.fromisoformat(value) if value else None
    if isinstance(column.type, db.Time):
        return time.fromisoformat(value) if value else None
    if isinstance(column.type, db.DateTime):
        return datetime.fromisoformat(value) if value else None
    if isinstance(column.type, db.Boolean):
        return value in ("1", "true", "True", "on", "yes", "Yes")
    return value

def build_object(model, form, existing=None):
    obj = existing or model()
    for column in model.__table__.columns:
        if column.name == "id" or column.name in ("created_at", "updated_at"):
            continue
        if column.name in form:
            setattr(obj, column.name, parse_value(column, form.get(column.name)))
    return obj
