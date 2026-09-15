from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import LostFound

lost_found_bp = Blueprint("lost_found", __name__, url_prefix="/lost-found")

@lost_found_bp.route("/")
@login_required
def index():
    reports = LostFound.query.filter_by(user_id=current_user.id).order_by(LostFound.created_at.desc()).all()
    return render_template("lost_found/index.html", reports=reports)

@lost_found_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        report_type = request.form.get("report_type", "")
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        if report_type not in ("Lost", "Found") or not description or not location:
            flash("Report type, description and location are required.", "danger")
        else:
            report = LostFound(
                user_id=current_user.id, report_type=report_type,
                description=description, location=location
            )
            db.session.add(report)
            db.session.commit()
            flash(f"Lost & Found report created. Report ID: {report.id}", "success")
            return redirect(url_for("lost_found.index"))
    return render_template("lost_found/form.html")
