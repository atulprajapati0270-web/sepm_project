from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    contact = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Route(db.Model):
    __tablename__ = "routes"

    id = db.Column(db.Integer, primary_key=True)
    route_name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Open")
    restriction = db.Column(db.String(255))
    parking = db.Column(db.String(255))
    alternate_route = db.Column(db.String(255))
    details = db.Column(db.Text)


class Accommodation(db.Model):
    __tablename__ = "accommodations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    details = db.Column(db.Text)
    contact = db.Column(db.String(50))


class FoodFacility(db.Model):
    __tablename__ = "food_facilities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    details = db.Column(db.Text)
    contact = db.Column(db.String(50))


class MedicalFacility(db.Model):
    __tablename__ = "medical_facilities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(50))
    service_details = db.Column(db.Text)


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    location = db.Column(db.String(150))
    description = db.Column(db.Text)


class ShahiSnan(db.Model):
    __tablename__ = "shahi_snan"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    location = db.Column(db.String(150))
    instructions = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)
    verification_note = db.Column(db.Text)


class SecurityInfo(db.Model):
    __tablename__ = "security_info"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    police_help_point = db.Column(db.String(150))
    safety_information = db.Column(db.Text)
    alert_level = db.Column(db.String(50), default="Normal")


class Temple(db.Model):
    __tablename__ = "temples"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)


class EmergencyHelpline(db.Model):
    __tablename__ = "emergency_helplines"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)


class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150))
    status = db.Column(db.String(50), default="Submitted")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("complaints", lazy=True))


class LostFound(db.Model):
    __tablename__ = "lost_found"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    report_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), default="Reported")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("lost_found_reports", lazy=True))


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(50), default="Normal")
    date = db.Column(db.DateTime, default=datetime.utcnow)


class AdminLog(db.Model):
    __tablename__ = "admin_logs"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship("User", backref=db.backref("admin_logs", lazy=True))