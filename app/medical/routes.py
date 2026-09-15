from flask import Blueprint, render_template, request
from ..models import MedicalFacility

medical_bp = Blueprint("medical", __name__, url_prefix="/medical")

@medical_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = MedicalFacility.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [MedicalFacility.route_name],
            "accommodation": [MedicalFacility.name, MedicalFacility.type, MedicalFacility.location],
            "food": [MedicalFacility.name, MedicalFacility.category, MedicalFacility.location],
            "medical": [MedicalFacility.name, MedicalFacility.type, MedicalFacility.location],
            "events": [MedicalFacility.name, MedicalFacility.location, MedicalFacility.description],
            "shahi_snan": [MedicalFacility.location, MedicalFacility.instructions],
            "security": [MedicalFacility.title, MedicalFacility.safety_information],
            "temples": [MedicalFacility.name, MedicalFacility.location, MedicalFacility.description],
            "emergency": [MedicalFacility.category, MedicalFacility.number, MedicalFacility.details],
            "notifications": [MedicalFacility.title, MedicalFacility.message, MedicalFacility.priority],
        }["medical"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(MedicalFacility, "name").desc() if "medical" in ["events","shahi_snan","notifications"] else getattr(MedicalFacility, "name")).all()
    return render_template("medical/medical.html", items=items, title="Medical Facilities", q=q)
