from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db, login_manager
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        contact = request.form.get("contact", "").strip()
        password = request.form.get("password", "")
        if not name or not email or not password:
            flash("Name, email and password are required.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
        else:
            user = User(name=name, email=email, contact=contact)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin.dashboard") if user.role == "admin" else url_for("main.home"))
        flash("Invalid email or password.", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.home"))

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.name = request.form.get("name", "").strip()
        current_user.contact = request.form.get("contact", "").strip()
        db.session.commit()
        flash("Profile updated.", "success")
    return render_template("auth/profile.html")
