from flask import Blueprint, render_template, request
from ..models import FoodFacility

food_bp = Blueprint("food", __name__, url_prefix="/food")

@food_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    query = FoodFacility.query
    if q:
        # Module-specific search across common fields
        search_fields = {
            "traffic": [FoodFacility.route_name],
            "accommodation": [FoodFacility.name, FoodFacility.type, FoodFacility.location],
            "food": [FoodFacility.name, FoodFacility.category, FoodFacility.location],
            "medical": [FoodFacility.name, FoodFacility.type, FoodFacility.location],
            "events": [FoodFacility.name, FoodFacility.location, FoodFacility.description],
            "shahi_snan": [FoodFacility.location, FoodFacility.instructions],
            "security": [FoodFacility.title, FoodFacility.safety_information],
            "temples": [FoodFacility.name, FoodFacility.location, FoodFacility.description],
            "emergency": [FoodFacility.category, FoodFacility.number, FoodFacility.details],
            "notifications": [FoodFacility.title, FoodFacility.message, FoodFacility.priority],
        }["food"]
        from sqlalchemy import or_
        query = query.filter(or_(*[field.ilike(f"%{q}%") for field in search_fields]))
    items = query.order_by(getattr(FoodFacility, "name").desc() if "food" in ["events","shahi_snan","notifications"] else getattr(FoodFacility, "name")).all()
    return render_template("food/food.html", items=items, title="Food Facilities", q=q)
