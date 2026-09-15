from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Complaint

complaints_bp = Blueprint("complaints", __name__, url_prefix="/complaints")

@complaints_bp.route("/")
@login_required
def index():
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template("complaints/index.html", complaints=complaints)

@complaints_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        if not category or not description:
            flash("Category and description are required.", "danger")
        else:
            complaint = Complaint(
                user_id=current_user.id, category=category,
                description=description, location=location
            )
            db.session.add(complaint)
            db.session.commit()
            flash(f"Complaint submitted successfully. Complaint ID: {complaint.id}", "success")
            return redirect(url_for("complaints.index"))
    return render_template("complaints/form.html")
