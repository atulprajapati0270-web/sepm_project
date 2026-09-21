from flask import Blueprint, render_template, request
from ..models import MedicalFacility

medical_bp = Blueprint("medical", __name__, url_prefix="/medical")

@medical_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = MedicalFacility.query
    if q:
        search_fields = [MedicalFacility.name, MedicalFacility.type, MedicalFacility.location, MedicalFacility.service_details]
        from ..extensions import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(MedicalFacility, "name").desc() if "medical" in ["events","shahi_snan","notifications"] else getattr(MedicalFacility, "name")).all()
    return render_template("medical/medical.html", items=items, title="Medical Facilities", q=q)
